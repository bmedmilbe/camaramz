"""String formatting and text generation utilities for certificate documents.

This module provides helper methods for generating properly formatted Portuguese-language
text for certificates. Includes utilities for converting numbers to words, formatting
dates, handling gender agreement in Portuguese (o/a endings), and generating biographical
text from person records.

Classes:
    StringHelper: Static utility class for string formatting and text generation.
"""

from certificates.classes.interfaces.document import Document
from certificates.models import CertificateDate, CertificateTitle, CertificateTypes, Person, Street
from certificates.models import House
from datetime import datetime
from num2words import num2words
from pprint import pprint


class StringHelper():
    """Utility class for Portuguese text formatting and certificate text generation.

    Provides static methods for:
    - Converting numbers to Portuguese words (with hyphenated numbers support)
    - Formatting dates in Portuguese long/short forms
    - Handling Portuguese gender agreement in text (o/a, filho/filha, etc)
    - Generating biographical text from person records
    - Building address strings from location data
    - Creating formatted person lists with proper conjunctions
    """

    def readNumber(self, string):
        """Convert numeric values in a string to Portuguese words.

        Args:
            string (str): Text string containing numbers and words.

        Returns:
            str: String with numeric values converted to Portuguese words.
        """
        final_text = ""
        dados = string.split()

        for value in dados:
            text = self.NumeroEmExtenso(value) if value.isnumeric() else value
            final_text = f"{final_text} {text}"

        return final_text

    def NumeroEmExtenso(number):
        """Convert number to Portuguese text representation (extenso).

        Handles regular numbers and hyphenated numbers (e.g., "123-456" becomes
        "cento e vinte e três - quatrocentos e cinquenta e seis").

        Args:
            number (int or str): Number to convert, may include hyphens.

        Returns:
            str: Number written in Portuguese words.
        """
        if '-' not in str(number):
            return num2words(number, lang='pt')
        text = ''
        for item in str(number).split('-'):
            if str(item).isnumeric():
                text = f"{text}{num2words(item, lang='pt')} "
            else:
                text = f"{text} {item} "

        return text[:-1]

    def houseNumber(self, house_number):
        """Format house number/identifier for certificate text.

        Args:
            house_number (str): House number identifier (may be numeric or alphanumeric).

        Returns:
            str: Formatted house number text in Portuguese (e.g., " na casa número X, ").
                 Returns "numa casa não numerada" if house_number is None/missing.
        """
        if not house_number or house_number is None or house_number == -1 or house_number == "-1":
            return f" numa casa não numerada, "

        if house_number.isnumeric():
            return f" na casa número {self.NumeroEmExtenso(house_number)}" ", "

        elif house_number:
            house_number = f" na casa número {self.readNumber(self,house_number)}, "

        return house_number

    def NumeroCompleto(self, number):
        """Get complete number text representation.

        Args:
            number (int or str): Number to convert.

        Returns:
            str: Full number text in Portuguese.
        """
        return self.readNumber(number)

    def separateString(self, string):
        """Separate characters in a string with spaces.

        Args:
            string (str): Input string.

        Returns:
            str: String with spaces between each character.
        """
        string_n = ""

        for i in range(len(string)):
            string_n = f"{string_n} {string[i]}"
            if i < len(string) - 1:
                string_n = f'{string_n} '

        return string_n

    def text_bi(self, certificate_type: CertificateTypes, bi1: Person, bi2: Person = None, data=None):
        """Generate biographical text for one or two persons (primary and secondary).

        Args:
            certificate_type (CertificateTypes): Type of certificate (determines text format).
            bi1 (Person): Primary person record.
            bi2 (Person, optional): Secondary person record (e.g., spouse). Defaults to None.
            data (dict, optional): Additional context data. Defaults to None.

        Returns:
            str: Formatted biographical text in Portuguese.
        """
        substring = ""
        if bi2:
            substring = f"{self.text(self,bi2, certificate_type)} a favor de, "

        return f"{substring} {self.text(self, bi1, certificate_type, data)}"

    def text(self, bi: Person, certificate_type, data=None):
        """Generate formal biographical description of a person for certificates.

        Includes full name, civil status, birthplace, birth date, parents' names,
        ID information, and other biographical details depending on certificate type.
        Text properly handles Portuguese gender agreement (male/female endings).

        Args:
            bi (Person): Person record with biographical data.
            certificate_type (CertificateTypes): Type of certificate (affects content).
            data (dict, optional): Additional context data (nationality, etc). Defaults to None.

        Returns:
            str: Formatted biographical text in Portuguese with proper gender agreement.
        """
        vivo = ""
        naturalidade = f"{bi.birth_address}"

        if certificate_type.id == 15 or certificate_type.id == 10 or certificate_type.id == 22:
            vivo = f' vitalício, é viv{StringHelper.oa(self,bi.gender)} e '

        if certificate_type.id == 9 and not data:
            naturalidade = f"{bi.birth_address.birth_country.name}, de nacionalidade {data.nationality}"

        return f"{self.toBold(bi.name)} {self.toBold(bi.surname)}, {self.estado( bi)}, natural de {naturalidade}, nascid{StringHelper.oa(self, bi.gender)} em {self.ext_data(self, bi.birth_date)}, filh{StringHelper.oa(self, bi.gender)} de {self.toBold(self.pais(self, bi))}, portador{self.oa2(self, bi.gender)} do {bi.id_type.name} número {self.NumeroEmExtenso(bi.id_number)}, passado pelo {bi.id_issue_local.name}, aos { self.ext_data(self, bi.id_issue_date)},{vivo}"

    def pais(self, bi: Person):
        """Get formatted parent names for biographical text.

        Args:
            bi (Person): Person record with father/mother names.

        Returns:
            str: Formatted parent names ("father and mother" / "father" / "mother").
        """
        if bi.father_name and bi.mother_name:
            fathers = f"{bi.father_name} e de {bi.mother_name}"
        elif bi.father_name and not bi.mother_name:
            fathers = f"{bi.father_name}"
        else:
            fathers = f"{bi.mother_name}"

        return fathers

    def house_address(self, house: House):
        """Format complete house address for certificate text.

        Args:
            house (House): House model with street and location data.

        Returns:
            str: Formatted address in Portuguese (e.g., "na casa número X, na localidade de Street, Distrito de County").
        """
        return f"{self.houseNumber(self,house.house_number)} na localidade de {house.street.name}, Distrito de {house.street.town.county.name}"

    def street_address(self, street: Street):
        """Format street/locality address for certificate text.

        Args:
            street (Street): Street model with town and county data.

        Returns:
            str: Formatted address in Portuguese (e.g., "na localidade de Street, Distrito de County").
        """
        return f"na localidade de {street.name}, Distrito de {street.town.county.name}"

    def simple_person_text(self, persons):
        """Generate formatted list of persons with birth dates and conjunctions.

        Args:
            persons (QuerySet): QuerySet of Person objects.

        Returns:
            str: Formatted text like "de John, nascido em ..., de Jane, nascida em ..., e de Mary, nascida em ...".
        """
        text = ""
        count = persons.count()
        index = 0
        for person in persons.all():
            index = index + 1
            de_or_virgula = ", "
            if index == count - 1:
                de_or_virgula = " e"
            text = f"{text} d{StringHelper.oa(StringHelper,person.gender)} {StringHelper.toBold(person.name)}, nascid{StringHelper.oa(StringHelper,person.gender)} em {StringHelper.ext_data(StringHelper,person.birth_date)}{de_or_virgula} "
        return text

    def simple_parent_text(self, parents):
        """Generate formatted text describing parent/family relationships.

        Groups family members by relationship type, handles singular/plural agreement,
        and formats with proper Portuguese conjunctions.

        Args:
            parents (QuerySet): QuerySet of CertificateSimpleParent objects.

        Returns:
            str: Formatted family relationship text (e.g., "seu pai, John, nascido em ..., e sua mãe, Jane, nascida em ...").
        """
        text = ""
        count = parents.count()
        index = 0

        members = dict()

        for person in parents.all():
            members[person.parent.degree] = members[person.parent.degree] + \
                [person] if members.get(person.parent.degree) else [person]

        members = dict(sorted(members.items()))

        bemcomo = ""
        for member in members.keys():
            if bemcomo == "" and member > 3:
                bemcomo = "bem como "
                text = f"{text} {bemcomo}"

            qtd = len(members[member])
            his = f"suas {members[member][0].parent.in_plural}, "
            if qtd == 1:
                his = f"seu {members[member][0].parent.title}, " if members[member][
                    0].parent.gender == "M" else f"sua {members[member][0].parent.title}, "
            if qtd >= 2:
                for single_member in members[member]:
                    if single_member.parent.gender == "M":
                        his = f"seus {members[member][0].parent.in_plural_mix}, "
            text = f"{text}{his}"
            index = 0
            count = len(members[member])
            for single_member in members[member]:
                index = index + 1
                de_or_virgula = ", "
                if index == count - 1:
                    de_or_virgula = ", e "

                text = f"{text}{StringHelper.toBold(single_member.name)}, nascid{StringHelper.oa(StringHelper,single_member.parent.gender)} em {StringHelper.ext_data(StringHelper,single_member.birth_date)}{de_or_virgula}"

        return text

    def calendar_month(month_number):
        """Get Portuguese month name from number.

        Args:
            month_number (int): Month number (1-12).

        Returns:
            str: Portuguese month name (e.g., "Janeiro", "Fevereiro").
        """
        months = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Março",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro",
        }

        return months.get(month_number)

    def dia(self, date):
        """Get zero-padded day from date.

        Args:
            date (datetime): Date object.

        Returns:
            str: Day formatted as "0X" or "X".
        """
        return "0" if date.dia < 10 else f"0{date.dia}"

    def mes(self, date):
        """Get zero-padded month from date.

        Args:
            date (datetime): Date object.

        Returns:
            str: Month formatted as "0X" or "X".
        """
        return "0" if date.month < 10 else f"0{date.month}"

    def data(self, date):
        """Format date as DD/MM/YYYY (short format).

        Args:
            date (datetime): Date to format.

        Returns:
            str: Date string in DD/MM/YYYY format.
        """
        return f"{date.day}/{date.month}/{self.NumeroEmExtenso( date.year)}"

    def ext_data(self, date):
        """Format date in extended Portuguese format (e.g., "15 de Março de 2024").

        Args:
            date (datetime): Date to format.

        Returns:
            str: Extended date in Portuguese (day in words, month name, year in words).
        """
        return f"{self.NumeroEmExtenso( date.day)} de {self.calendar_month(date.month)} de {self.NumeroEmExtenso( date.year)}"

    def ext_days(self, dates: CertificateDate):
        """Format multiple dates as extended list with proper conjunctions.

        Groups dates by month and formats with proper Portuguese conjunctions
        (commas, "e", "ou" as appropriate).

        Args:
            dates (QuerySet): QuerySet of CertificateDate objects.

        Returns:
            str: Formatted date list (e.g., "nos dias 5, 15, e 25 de Março de 2024, ...").
        """
        new_dates = dict()
        for month in dates.all():
            new_dates[month.date.month] = new_dates[month.date.month] + \
                [month] if new_dates.get(month.date.month) else [month]

        new_dates = dict(sorted(new_dates.items()))
        text = ""
        count_super = 0
        text = f" nos dias " if dates.count() > 1 else " no dia "
        for month in new_dates.keys():
            qtd = len(new_dates[month])

            if qtd == 1:
                e = ", e " if count_super + 1 == dates.count() - 1 else ", "

                text = f"{text}{self.ext_data(self,new_dates[month][0].date)}{e}"
                count_super = count_super + 1
            if qtd >= 2:
                text = f"{text}"
                index = 0
                count = len(new_dates[month])
                if count_super > 0:
                    text = f"{text} e "

                for single_date in new_dates[month]:
                    count_super = count_super + 1
                    index = index + 1
                    de_or_virgula = "" if index == count else ", "
                    if index == count - 1:
                        de_or_virgula = ", e "
                    text = f"{text}{self.NumeroEmExtenso(single_date.date.day)}{de_or_virgula}"

                text = f"{text} de {self.calendar_month(int(new_dates[month][0].date.month))} de {self.NumeroEmExtenso(new_dates[month][0].date.year)}, "

        return text

    def get_string_between(string, start, end):
        """Extract substring between two delimiters (utility method).

        Args:
            string (str): Source string.
            start (str): Starting delimiter.
            end (str): Ending delimiter.

        Returns:
            str: Substring between delimiters, or empty string if not found.
        """
        string = f' {string}'
        ini = strpos(string, start)
        if ini == 0:

    def house_address(self, house: House):

        return f"{self.houseNumber(self,house.house_number)} na localidade de {house.street.name}, Distrito de {house.street.town.county.name}"

    def street_address(self, street: Street):

        return f"na localidade de {street.name}, Distrito de {street.town.county.name}"

    def simple_person_text(self, persons):
        text = ""
        # pprint(persons.all())
        count = persons.count()
        index = 0
        for person in persons.all():
            index = index + 1
            de_or_virgula = ", "
            if index == count - 1:
                de_or_virgula = " e"
            text = f"{text} d{StringHelper.oa(StringHelper,person.gender)} {StringHelper.toBold(person.name)}, nascid{StringHelper.oa(StringHelper,person.gender)} em {StringHelper.ext_data(StringHelper,person.birth_date)}{de_or_virgula} "
        return text

    def simple_parent_text(self, parents):
        text = ""
        # pprint(persons.all())
        count = parents.count()
        index = 0

        members = dict()

        for person in parents.all():
            members[person.parent.degree] = members[person.parent.degree] + \
                [person] if members.get(person.parent.degree) else [person]

        members = dict(sorted(members.items()))

        bemcomo = ""
        for member in members.keys():
            # pprint(len(members[member]))
            if bemcomo == "" and member > 3:
                bemcomo = "bem como "
                text = f"{text} {bemcomo}"

            qtd = len(members[member])
            his = f"suas {members[member][0].parent.in_plural}, "
            if qtd == 1:
                his = f"seu {members[member][0].parent.title}, " if members[member][
                    0].parent.gender == "M" else f"sua {members[member][0].parent.title}, "
            if qtd >= 2:
                for single_member in members[member]:
                    if single_member.parent.gender == "M":
                        his = f"seus {members[member][0].parent.in_plural_mix}, "
            text = f"{text}{his}"
            index = 0
            count = len(members[member])
            for single_member in members[member]:
                index = index + 1
                de_or_virgula = ", "
                if index == count - 1:
                    de_or_virgula = ", e "

                text = f"{text}{StringHelper.toBold(single_member.name)}, nascid{StringHelper.oa(StringHelper,single_member.parent.gender)} em {StringHelper.ext_data(StringHelper,single_member.birth_date)}{de_or_virgula}"

            # text = f"{text} "

        # pprint(text)
        return text
        for person in parents.all():
            index = index + 1
            de_or_virgula = ", "
            if index == count - 1:
                de_or_virgula = " e"
            text = f"{text} {StringHelper.oa(StringHelper,person.gender)} {StringHelper.toBold(person.name)}, nascid{StringHelper.oa(StringHelper,person.gender)} em {StringHelper.ext_data(StringHelper,person.birth_date)}{de_or_virgula} "
        return text

    def calendar_month(month_number):
        months = {
            1: "Janeiro",
            2: "Fevereiro",
            3: "Março",
            4: "Abril",
            5: "Maio",
            6: "Junho",
            7: "Julho",
            8: "Agosto",
            9: "Setembro",
            10: "Outubro",
            11: "Novembro",
            12: "Dezembro",
        }

        # pprint("Mes")
        # pprint(month_number)
        return months.get(month_number)

    def dia(self, date):
        return "0" if date.dia < 10 else f"0{date.dia}"

    def mes(self, date):
        return "0" if date.month < 10 else f"0{date.month}"

    def data(self, date):
        return f"{date.day}/{date.month}/{self.NumeroEmExtenso( date.year)}"

    def ext_data(self, date):
        return f"{self.NumeroEmExtenso( date.day)} de {self.calendar_month(date.month)} de {self.NumeroEmExtenso( date.year)}"

    def ext_days(self, dates: CertificateDate):

        new_dates = dict()
        for month in dates.all():
            new_dates[month.date.month] = new_dates[month.date.month] + \
                [month] if new_dates.get(month.date.month) else [month]

        new_dates = dict(sorted(new_dates.items()))
        text = ""
        count_super = 0
        text = f" nos dias " if dates.count() > 1 else " no dia "
        for month in new_dates.keys():
            # pprint(new_dates[month])
            qtd = len(new_dates[month])

            if qtd == 1:
                e = ", e " if count_super + 1 == dates.count() - 1 else ", "

                text = f"{text}{self.ext_data(self,new_dates[month][0].date)}{e}"
                count_super = count_super + 1
            if qtd >= 2:
                text = f"{text}"
                index = 0
                count = len(new_dates[month])
                if count_super > 0:
                    text = f"{text} e "

                for single_date in new_dates[month]:
                    count_super = count_super + 1
                    index = index + 1
                    de_or_virgula = "" if index == count else ", "
                    if index == count - 1:
                        de_or_virgula = ", e "
                    text = f"{text}{self.NumeroEmExtenso(single_date.date.day)}{de_or_virgula}"

                text = f"{text} de {self.calendar_month(int(new_dates[month][0].date.month))} de {self.NumeroEmExtenso(new_dates[month][0].date.year)}, "

        return text

    def get_string_between(string, start, end):
        string = f' {string}'
        ini = strpos(string, start)
        if ini == 0:
            return ''
        ini = ini + strlen(start)
        len = strpos(string, end, ini) - ini
        return substr(string, ini, len)

    def dateShow(stamp):
        return f"{GetFromStamp(stamp,'d')}-{GetFromStamp(stamp,'M')}-{GetFromStamp(stamp,'Y')}"

    def sanitize(dirty):

        return dirty

    def GetDateTime(time):
        if time:
            return (date("Y-m-d H:i:s", time))

        return time

    def GetFromStamp(stamp, pos):

        d = DateTime(stamp)

        time = d.getTimestamp()

        if time:
            return (date(pos, time))

        return time

    def currentUser():

        return Users.currentLoggedInUser()

    def posted_values(post):
        clean_ary = []
        # uncomment and implement
        # foreach(post as key => value){
        #     if(is_array(value)){
        #         foreach(value as k => v){
        #             clean_ary[key][k] = sanitize(v)
        #         }
        #     }else{
        #         clean_ary[key] = sanitize(value)
        #     }
        # }
        return clean_ary

    def currentPage():
        currentPage = _SERVER['REQUEST_URI']
        if currentPage == PROOT or currentPage == f"{PROOT}.'home/index":
            currentPage = f"{PROOT}home"

        return currentPage

    def postsanitize(array):
        # uncoment and implement
        # foreach(array as key => value){
        #     if(is_array(value)){
        #         foreach(value as k => v){
        #             _POST[key][k] = sanitize(v)
        #         }
        #     }else{
        #         _POST[key] = sanitize(value)
        #     }

        # }
        pass

    def sanitizearray(array):
        # uncomment
        # foreach(array as key => value){
        #     array[key] = sanitize(value)
        # }
        return array

    # //Gera chave userkey

    def KeyGenerator():

        return sha1(rand() . time())
        # //sha1 nap pode ser descriptografada

    def setNumber(atestado_casa):

        final_text = ""
        dados = explode(' ', atestado_casa)
        # //dnd(dados)
        # uncomment
        # foreach (dados as key => value) {
        #     if (is_numeric(value)) {
        #         text = NumeroEmExtenso(value)
        #     } else {
        #         text = value
        #     }
        #     final_text .= " " . text
        # }
        atestado_casa = final_text

        return atestado_casa

    def estado(bi):

        # pprint(bi.status)
        # pprint(bi.gender)
        # bi.status
        result = ""
        oa = "o" if bi.gender == "M" else "a"

        if bi.status == "S":
            result = f"Solteir{oa}"
        elif bi.status == "M":
            result = f"Casad{oa}"
        elif bi.status == "L":
            result = f"Em comunhão de factos"
        elif bi.status == "V":
            result = f"Viúv{oa}"
        elif bi.status == "D":
            result = f"Divociad{oa}"

        return result

    def oa(self, genero):
        return "o" if genero == "M" else "a"

    def oa2(self, genero):
        return "" if genero == "M" else "a"

    def oa3(self, genero):
        return "" if genero == "M" else "à"

    def oa4(self, genero):
        return "ao" if genero == "M" else "à"

    def bi_sexo(self, genero):
        return "masculino" if genero == "M" else "feminino"

    def NumeroCompleto(atestado_casa):
        final_text = ""
        dados = explode(' ', atestado_casa)
        # //dnd(dados)

        # uncoment and implement
        # foreach (dados as key => value) {
        #     if (is_numeric(value)) {
        #         text = NumeroEmExtenso(value)
        #     } else {
        #         text = value
        #     }
        #     final_text .= " " . text
        # }
        return final_text

    def toBold(full_name):

        if isinstance(full_name, str):
            names = full_name.split(" ")
            string = ''
            count = 0
            for name in names:
                count = count + 1
                space = " " if count < len(names) else ""
                string = f"{string}@{name}#{space}"

            return f'{string}'
        return ""

    # def NumeroEmExtenso(numero):
    #     #uncomment and implremnt
    #     # F = new NumberFormatter("pt-PT",NumberFormatter::SPELLOUT)

    #     milhao = ""

    #     if(numero >= 1000000):

    #         milhao = intval(resto1 = numero / 1000000)

    #         numero = resto2 = numero - (milhao * 1000000)

    #         if(numero > 0):
    #             milhao = F.format(milhao * 1000000)

    #         else:
    #             return F.format(milhao * 1000000)

    #         if(numero > 1000000):
    #             # // millhos = intval(numero/1000000)
    #             pass

    #         mil = intval(numero/1000)

    #         resto = numero - (mil * 1000)

    #         if resto % 100 == 0 or resto <= 99:
    #             e = " e "
    #         else:
    #             e = ", "

    #         if resto != 0:
    #             milnumber = "" if mil == 1 else f"{F.format(mil)} mil {e} {F.format(resto)}"

    #             milnumber = milnumber if milhao == "" else f"{milhao}, {milnumber}"
    #             return milnumber

    #         else:

    #             milnumber = "" if mil == 1 else f"{F.format(mil)} {mil}"

    #             milnumber = milnumber if milhao == "" else f"{milhao} e {milnumber}"
    #             return milnumber

    #     return F.format(numero) if milhao == "" else f"{milhao} e {F.format(numero)}"

    #     # //F = new NumberFormatter("pt-PT",NumberFormatter::DEFAULT_STYLE)

    def DataEmExtenso(dia, mes, ano):
        text = f" em  {NumeroEmExtenso(dia)} de {mes} de {NumeroEmExtenso(ano)}"
        return text

    def encode(value):
        return utf8_encode(value)

    def decode(value):
        return utf8_decode(value)

    def renderText(model: Document):
        return model.create_text()
