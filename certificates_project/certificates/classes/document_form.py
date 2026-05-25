# from certificates.models import Country

class DocumentForm ():
   def __str__(self, form):
      
      pass
  
        # StringHelper = new StringHelper();


        # self.tipo = new Autocreatetype(
        #     isset(form['tipo']) ? form['tipo'] : ""
        # );
        
        
        # self.country = Country.objects.filter(id=form.get('country')).first()

        # self.modifics = new Modifics(
        #     isset(form.get('modific')) ? form.get('modific') : ""
        # );

        # self.localidade1 = new Localidades(
        #     isset(form.get('localidade-1')) ? form.get('localidade-1') : ""
        # );
        # self.coval_data = new Covals(
        #     isset(form.get('coval_id')) ? form.get('coval_id') : ""
        # );

        # self.house = isset(form.get('house')) ? form.get('house') : "";
        # self.infra = isset(form.get('infra')) ? form.get('infra') : "";
        # self.dias = isset(form.get('dias')) ? form.get('dias') : "";
        # self.metros = isset(form.get('metros')) ? form.get('metros') : "";
        # self.data3 = isset(form.get('data3')) ? form.get('data3') : "";
        # self.house_ext = self.houseNumber(
        #     isset(form.get('house')) ? form.get('house') : ""
        #     );
        # self.localidade = new Localidades(
        #     isset(form.get('localidade')) ? form.get('localidade') : ""
        #     );
        # self.entidade = new Entidades(
        #     isset(form.get('entidade')) ? form.get('entidade') : ""
        #     ); # Institution
        # self.univer = new Univers(
        #     isset( form.get('univer')) ?  form.get('univer') : ""
        #    );
        # self.nas_date = new Dates(
        #     isset( form.get('nas-dia')) ?  form.get('nas-dia') : "",
        # isset( form.get('nas-mes')) ?  form.get('nas-mes') : "",
        #     isset( form.get('nas-ano')) ?  form.get('nas-ano') : ""
        # );
        # self.nacionalidade = isset( form.get('nacionalidade')) ?  form.get('nacionalidade') : "";
        # self.instituicao = isset( form.get('instituicao')) ?  form.get('instituicao') : "";
        # self.desde = isset( form.get('desde')) ?  form.get('desde') : "";
        # self.objecto = isset( form.get('objecto')) ?  form.get('objecto') : "";

        # //var_dump(self.desde);

        # self.demo1 = isset(form.get('demo1')) &&  is_numeric(form.get('demo1')) ?  intval(form.get('demo1')) : 0;
        # //dnd(self.demo1);
        # for(i = 1; i <= self.demo1; i++){
        #     self.person[i] = new Person(i, form);
        # }

        # self.causa = isset( form.get('causa')) ?  form.get('causa') : "";
        # self.nome1 = isset( form.get('nome-1')) ?  form.get('nome-1') : "";
        # self.genero1 = isset( form.get('genero-1')) ?  form.get('genero-1') : "";
        # self.oa1 = self.genero1 == 1 ? "o" : "a";
        # self.oa = self.genero1 == 1 ? "" : "a";


        # self.nome2 = isset( form.get('nome-2')) ?  form.get('nome-2') : "";
        # self.genero2 = isset( form.get('genero-2')) ?  form.get('genero-2') : "";
        # self.oa21 = self.genero2 == 1 ? "o" : "a";
        # self.oa2 = self.genero2 == 1 ? "" : "a";

        # self.nome3 = isset( form.get('nome-3')) ?  form.get('nome-3') : "";
        # self.genero3 = isset( form.get('genero-3')) ?  form.get('genero-3') : "";
        # self.oa31 = self.genero3 == 1 ? "o" : "a";
        # self.oa3 = self.genero3 == 1 ? "" : "a";


        # self.profissao = isset( form.get('profissao')) ?  form.get('profissao') : "";


        # self.total = 0;
        # self.total += self.filhos = isset( form.get('filhos')) && is_numeric(form.get('filhos')) ?  intval(form.get('filhos')) : 0;
        # for(i = 1; i <= self.filhos; i++){
        #     self.filho[i] = new Person(i, form, 'filh');
        # }

        # self.total += self.netos = isset( form.get('netos')) && is_numeric(form.get('netos')) ?  form.get('netos') : 0;
        # for(i = 1; i <= self.netos; i++){
        #     self.neto[i] = new Person(i, form, 'net');
        # }


        # self.total += self.primos = isset( form.get('primos')) && is_numeric(form.get('primos')) ?  form.get('primos') : 0;
        # for(i = 1; i <= self.primos; i++){
        #     self.primo[i] = new Person(i, form, 'prim');
        # }

        # self.total += self.sogros = isset( form.get('sogros')) && is_numeric(form.get('sogros')) ?  form.get('sogros') : 0;
        # for(i = 1; i <= self.sogros; i++){
        #     self.sogro[i] = new Person(i, form, 'sogr');
        # }

        # self.total += self.irmaos = isset( form.get('irmaos')) && is_numeric(form.get('irmaos')) ?  form.get('irmaos') : 0;
        # for(i = 1; i <= self.irmaos; i++){
        #     self.irmao[i] = new Person(i, form, 'irm');
        # }

        # self.total += self.cunhados = isset( form.get('cunhados')) && is_numeric(form.get('cunhados')) ?  form.get('cunhados') : 0;
        # for(i = 1; i <= self.cunhados; i++){
        #     self.cunhado[i] = new Person(i, form, 'cunhad');
        # }

        # self.total += self.sobrinhos = isset( form.get('sobrinhos')) && is_numeric(form.get('sobrinhos')) ?  form.get('sobrinhos') : 0;
        # for(i = 1; i <= self.sobrinhos; i++){
        #     self.sobrinho[i] = new Person(i, form, 'subrinh');
        # }

        # self.total += self.entiados = isset( form.get('entiados')) && is_numeric(form.get('entiados')) ?  form.get('entiados') : 0;
        # for(i = 1; i <= self.entiados; i++){
        #     self.entiado[i] = new Person(i, form, 'entiad');
        # }

        # self.total += self.tios = isset( form.get('tios')) && is_numeric(form.get('tios')) ?  form.get('tios') : 0;
        # for(i = 1; i <= self.tios; i++){
        #     self.tio[i] = new Person(i, form, 'ti');
        # }

        # self.total += self.avo = isset( form.get('avo')) && is_numeric(form.get('avo')) ?  form.get('avo') : 0;
        # for(i = 1; i <= self.avo; i++){
        #     self.avos[i] = new Person(i, form, 'av');
        # }

        # self.total += self.companheiro = isset( form.get('companheiro')) && is_numeric(form.get('companheiro')) ?  form.get('companheiro') : 0;
        # for(i = 1; i <= self.companheiro; i++){
        #     self.companheiros[i] = new Person(i, form, 'companheir');
        # }
        # //dnd(self.companheiros);
        # //var_dump(self.companheiro);
        # //dnd(self.companheiros);

        # self.total += self.afillhados = isset( form.get('afillhados')) && is_numeric(form.get('afillhados')) ?  form.get('afillhados') : 0;
        # for(i = 1; i <= self.afilhados; i++){
        #     self.afilhado[i] = new Person(i, form, 'afilhad');
        # }



        # self.pai = isset( form.get('pai')) ?  intval(form.get('pai')) : 0;
        # self.total = self.pai = self.pai == 1 ?  1 : 0;
        # for(i = 1; i <= self.pai; i++){
        #     self.pai1[i] = new Person(i, form, 'pai');
        # }
        # self.mae = isset( form.get('mae')) ?  intval(form.get('mae')) : 0;
        # self.total = self.mae = self.mae == 1 ?  1 : 0;
        # for(i = 1; i <= self.mae; i++){
        #     self.mae1[i] = new Person(i, form, 'mae');
        # }


        # self.coval2 = isset(form.get('coval2'))  ?  form.get('coval2') : "";
        # self.coval_name2 = isset(form.get('coval2'))  ?  StringHelper.NumeroCompleto(form.get('coval2')) : "";
        # self.ano2 = isset(form.get('ano2'))  ?  form.get('ano2') : "";
        # self.ano_name2 = isset(form.get('ano2'))  ?  StringHelper.NumeroCompleto(form.get('ano2')) : "";



        # self.coval = isset(form.get('coval'))  ?  form.get('coval') : "";
        # self.coval_name = isset(form.get('coval'))  ?  StringHelper.NumeroCompleto(form.get('coval')) : "";
        # self.ano = isset(form.get('ano'))  ?  form.get('ano') : "";
        # self.ano_name = isset(form.get('ano'))  ?  StringHelper.NumeroCompleto(form.get('ano')) : "";



        # self.cemiterio =
        #     new Cemiterios(
        #         isset(form.get('cemiterio')) ? form.get('cemiterio') : ""
        #     );
        # self.data1 =
        #     new Dates(
        #         isset(form.get('data1-dia')) ? form.get('data1-dia') : "",
        #         isset(form.get('data1-mes')) ? form.get('data1-mes') : "",
        #         isset(form.get('data1-ano')) ? form.get('data1-ano') : ""
        #     );
        # self.data2 =
        #     new Dates(
        #         isset(form.get('data2-dia')) ? form.get('data2-dia') : "",
        #         isset(form.get('data2-mes')) ? form.get('data2-mes') : "",
        #         isset(form.get('data2-ano')) ? form.get('data2-ano') : ""
        #     );

        # self.data4 =
        #     new Dates(
        #         isset(form.get('data4-dia')) ? form.get('data4-dia') : "",
        #         isset(form.get('data4-mes')) ? form.get('data4-mes') : "",
        #         isset(form.get('data4-ano')) ? form.get('data4-ano') : ""
        #     );
        # self.data5 =
        #     new Dates(
        #         isset(form.get('data5-dia')) ? form.get('data5-dia') : "",
        #         isset(form.get('data5-mes')) ? form.get('data5-mes') : "",
        #         isset(form.get('data5-ano')) ? form.get('data5-ano') : ""
        #     );

        # self.data6 =
        #     new Dates(
        #         isset(form.get('data6-dia')) ? form.get('data6-dia') : "",
        #         isset(form.get('data6-mes')) ? form.get('data6-mes') : "",
        #         isset(form.get('data6-ano')) ? $form.get('data6-ano') : ""
        #     );




#     }

#     /**
#      * @return Covals
#      */
#     public function getCovalData()
#     {
#         return $this.coval_data;
#     }

#     /**
#      * @return string
#      */
#     public function getCoval2()
#     {
#         return $this->coval2;
#     }

#     /**
#      * @return string
#      */
#     public function getCovalName2()
#     {
#         return $this->coval_name2;
#     }

#     /**
#      * @return string
#      */
#     public function getAno2()
#     {
#         return $this->ano2;
#     }

#     /**
#      * @return string
#      */
#     public function getAnoName2()
#     {
#         return $this->ano_name2;
#     }
    
#     public function getCountry()
#     {
#         return $this->country;
#     }



#     /**
#      * @return string
#      */
#     public function getData3()
#     {
#         return $this->data3;
#     }



#     /**
#      * @return string
#      */
#     public function getMetros()
#     {
#         return $this->metros;
#     }


#     /**
#      * @return string
#      */
#     public function getInfra()
#     {
#         return $this->infra;
#     }

#     /**
#      * @return string
#      */
#     public function getDias()
#     {
#         return $this->dias;
#     }

#     /**
#      * @return string
#      */
#     public function getOa()
#     {
#         return $this->oa;
#     }

#     /**
#      * @return mixed
#      */
#     public function getProfissao()
#     {
#         return $this->profissao;
#     }



#     /**
#      * @return mixed
#      */
#     public function getModifics()
#     {
#         return $this->modifics;
#     }

#     /**
#      * @return string
#      */
#     public function getObjecto()
#     {
#         return $this->objecto;
#     }




#     /**
#      * @return Dates
#      */
#     public function getData1()
#     {
#         return $this->data1;
#     }


#     /**
#      * @return Dates
#      */
#     public function getData2()
#     {
#         return $this->data2;
#     }
#     public function getData4()
#     {
#         return $this->data4;
#     }
#     public function getData5()
#     {
#         return $this->data5;
#     }

#     public function getData6()
#     {
#         return $this->data6;
#     }




#     /**
#      * @return string
#      */
#     public function getCoval()
#     {
#         return $this->coval;
#     }

#     /**
#      * @return string
#      */
#     public function getCovalName()
#     {
#         return $this->coval_name;
#     }

#     /**
#      * @return string
#      */
#     public function getAno()
#     {
#         return $this->ano;
#     }

#     /**
#      * @return string
#      */
#     public function getAnoName()
#     {
#         return $this->ano_name;
#     }

#     /**
#      * @return Cemiterios
#      */
#     public function getCemiterio()
#     {
#         return $this->cemiterio;
#     }



#     /**
#      * @return Autocreatetype
#      */
#     public function getTipo()
#     {
#         return $this->tipo;
#     }

#     /**
#      * @return Localidades
#      */
#     public function getLocalidade1()
#     {
#         return $this->localidade1;
#     }



#     /**
#      * @return string
#      */
#     public function getNome1()
#     {
#         return $this->nome1;
#     }

#     /**
#      * @return string
#      */
#     public function getGenero1()
#     {
#         return $this->genero1;
#     }

#     /**
#      * @return string
#      */
#     public function getOa1()
#     {
#         return $this->oa1;
#     }



#     /**
#      * @return int
#      */
#     public function getDemo1()
#     {
#         return $this->demo1;
#     }

#     /**
#      * @return mixed
#      */
#     public function getPerson($index)
#     {
#         return $this->person[$index];
#     }

#     /**
#      * @return string
#      */
#     public function getInstituicao()
#     {
#         return $this->instituicao;
#     }




#     /**
#      * @return string
#      */
#     public function getNacionalidade()
#     {
#         return $this->nacionalidade;
#     }



#     /**
#      * @return Dates
#      */
#     public function getNasDate()
#     {
#         return $this->nas_date;
#     }

#     /**
#      * @return Entidades
#      */
#     public function getEntidade()
#     {
#         return $this->entidade;
#     }

#     /**
#      * @return Univers
#      */
#     public function getUniver()
#     {
#         return $this->univer;
#     }


#     /**
#      * @return mixed
#      */
#     public function getHouse()
#     {
#         return $this->house;
#     }

#     /**
#      * @return mixed
#      */
#     public function getHouseExt()
#     {
#         return $this->house_ext;
#     }

#     /**
#      * @return mixed
#      */
#     public function getLocalidade()
#     {
#         return $this->localidade;
#     }

#     /**
#      * @return string
#      */
#     public function getDesde()
#     {
#         return $this->desde;
#     }

#     /**
#      * @return string
#      */
#     public function getNome2()
#     {
#         return $this->nome2;
#     }

#     /**
#      * @return string
#      */
#     public function getGenero2()
#     {
#         return $this->genero2;
#     }

#     /**
#      * @return string
#      */
#     public function getOa21()
#     {
#         return $this->oa21;
#     }

#     /**
#      * @return string
#      */
#     public function getOa2()
#     {
#         return $this->oa2;
#     }

#     /**
#      * @return string
#      */
#     public function getNome3()
#     {
#         return $this->nome3;
#     }

#     /**
#      * @return string
#      */
#     public function getGenero3()
#     {
#         return $this->genero3;
#     }

#     /**
#      * @return string
#      */
#     public function getOa31()
#     {
#         return $this->oa31;
#     }

#     /**
#      * @return string
#      */
#     public function getOa3()
#     {
#         return $this->oa3;
#     }


#     /**
#      * @return string
#      */
#     public function getNetos()
#     {
#         return $this->netos;
#     }

#     /**
#      * @return string
#      */
#     public function getSobrinhos()
#     {
#         return $this->sobrinhos;
#     }

#     /**
#      * @return string
#      */
#     public function getPrimos()
#     {
#         return $this->primos;
#     }

#     /**
#      * @return string
#      */
#     public function getSogros()
#     {
#         return $this->sogros;
#     }

#     /**
#      * @return string
#      */
#     public function getIrmaos()
#     {
#         return $this->irmaos;
#     }

#     /**
#      * @return string
#      */
#     public function getCunhados()
#     {
#         return $this->cunhados;
#     }

#     /**
#      * @return string
#      */
#     public function getCausa()
#     {
#         return $this->causa;
#     }

#     /**
#      * @return string
#      */

#     public function getEntiados()
#     {
#         return $this->entiados;
#     }

#     /**
#      * @return mixed
#      */
#     public function getAfilhados()
#     {
#         return $this->afilhados;
#     }

#     /**
#      * @return string
#      */
#     public function getTios()
#     {
#         return $this->tios;
#     }

#     /**
#      * @return string
#      */
#     public function getAvo()
#     {
#         return $this->avo;
#     }

#     /**
#      * @return string
#      */
#     public function getCompanheiro()
#     {
#         return $this->companheiro;
#     }

#     /**
#      * @return mixed
#      */
#     public function getCompanheiros()
#     {
#         return $this->companheiros;
#     }

#     /**
#      * @return mixed
#      */
#     public function getAvos()
#     {
#         return $this->avos;
#     }

#     /**
#      * @return mixed
#      */
#     public function getTio()
#     {
#         return $this->tio;
#     }

#     /**
#      * @return mixed
#      */
#     public function getAfilhado()
#     {
#         return $this->afilhado;
#     }

#     /**
#      * @return mixed
#      */
#     public function getEntiado()
#     {
#         return $this->entiado;
#     }

#     /**
#      * @return mixed
#      */
#     public function getCunhado()
#     {
#         return $this->cunhado;
#     }

#     /**
#      * @return mixed
#      */
#     public function getIrmao()
#     {
#         return $this->irmao;
#     }

#     /**
#      * @return mixed
#      */
#     public function getSogro()
#     {
#         return $this->sogro;
#     }

#     /**
#      * @return mixed
#      */
#     public function getPrimo()
#     {
#         return $this->primo;
#     }

#     /**
#      * @return mixed
#      */
#     public function getSobrinho()
#     {
#         return $this->sobrinho;
#     }

#     /**
#      * @return mixed
#      */
#     public function getNeto()
#     {
#         return $this->neto;
#     }

#     /**
#      * @return mixed
#      */
#     public function getMae1($index)
#     {
#         return $this->mae1[$index];
#     }

#     /**
#      * @return mixed
#      */
#     public function getPai1($index)
#     {
#         return $this->pai1[$index];
#     }

#     /**
#      * @return int
#      */
#     public function getPai()
#     {
#         return $this->pai;
#     }

#     /**
#      * @return int
#      */
#     public function getMae()
#     {
#         return $this->mae;
#     }

#     /**
#      * @return int
#      */
#     public function getTotal()
#     {
#         return $this->total;
#     }

#     /**
#      * @return mixed
#      */
#     public function getFilho()
#     {
#         return $this->filho;
#     }

#     /**
#      * @return mixed
#      */
#     public function getFilhos()
#     {
#         return $this->filhos;
#     }









# }