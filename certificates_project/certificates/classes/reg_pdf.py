
require_once("files/dompdf/autoload.inc.php");
use Dompdf\Dompdf;

class RegPDF
{
    public $pdf_root;
    public $pdf_name;
    public $pdf_number;

    public function __construct($text, $type1,AtestadoTypes $type2, Gerados $gerado, DocumentForm $form = null)
    {
        $dompdf = new DOMPDF();
        //dnd($form);

        $STYLE = $this->style();
        $HEAD = $this->head();


//$conta = "";
        $presidente = $this->setTracoLast(PRESIDENTE, $this->presidente());

        $string = $this->setTracoLast(CORPO, $text);

        $footer = $this->footer();


        $data = $this->data($gerado->getAtestadoDate());


        $html = "<!DOCTYPE html>
<html lang='pt'>

<body>

    $STYLE
    $HEAD


    <p class='p-left'>
        $presidente
     </p>

     <p class='p-left'>
        $string
    <br>
    </p>
    <p class='p-left'>
    $data
    </p>
    <p>
    $footer
    </p>

</body>
</html>";


        //echo $html;
        /**/
//echo $html;


        $dompdf->load_html($html);

//Renderizar o html

        $dompdf->render();


        $file_to_save = "files/gerados/" . $gerado->getAtestadoType1() . "/" . $gerado->getAtestadoType2() . "/" . $gerado->getAtestadoNumber() . ".pdf";


        file_put_contents($file_to_save, $dompdf->output());

        $this->pdf_root = $file_to_save;
        $this->pdf_name = $gerado->getAtestadoNumber() . ".pdf";
        $this->pdf_number = $gerado->getAtestadoNumber();
    }

    private function style()
    {
        $style = "
        <style>
        body{
            padding: 20px;

        }

        .name{
            font-weight: bold;
        }

        h1{
            text-align: center;
        }
        p{
            text-align: justify;
            font-size: 13.7pt;
        }


        .p-center{
            text-align: center;
        }
        .p-left{
            text-indent: 0;
            text-align: justify;
            font-size: 13.4pt;
        }
        .tittle{
        font-size: 12.5pt;
        }
        #p-flex{
             font-size: 12pt;
        }






         .ctable{
            width: 100%;
        }
        .ctable__row{
            width: 100%;
        }
        .ctable__d{
            text-align: center;

        }
        .ctable__d--40{
            width: 45%;
        }
        .ctable__d--20{
            width: 10%;
        }
        .ctable__d--right{

            text-align: right;

        }
        .ctable__d--left{
            text-align: left;
        }
        .ctable__d--img{
            width: 40px;
            height: auto;
        }



        .contas{
        text-align: right;
        }


        .conta__table{
            margin-top: 65px;
            width: 40%;
            float: right;



        }
        .conta__table__row{

        }
        .conta__table__th{

        }
        .conta__table__th--head{
            font-weight: 700;
            text-align: center;
        }
        .conta__table__th--title{
            font-weight: 400;
        }
        .conta__table__th--value{
            text-align: right;
            padding: 0;
        }

        .clear{
            clear: right;
        }



        .text-underline{
        text-decoration: underline;
        }
        .text-bold{
            font-weight: bold;
        }


    </style>



         ";

        return $style;
    }

    private function head()
    {

        $img = ROOT . '/files/fix/brasao.png';
        $text = "
<table class='ctable' id='header'>
    <tr class='ctable__row'>
        <td class='ctable__d ctable__d--40 ctable__d--right '>República Democrática</td>
        <td class='ctable__d ctable__d--20'>
            <img class='ctable__d--img' src='$img' alt='Brasao'>
        </td>
        <td class='ctable__d ctable__d--40 ctable__d--left'>de S. Tomé e Príncipe</td>
    </tr>
    <tr><td colspan='3' class='ctable__d'>(Unidade – Disciplina – Trabalho)</td></tr>
    <tr><td colspan='3' class='ctable__d'>CÂMARA DISTRITAL DE MÉ-ZÓCHI</td></tr>

</table>
";
        return $text;
    }

    private function conta(DocumentTypes $type1, AtestadoTypes $types2, $atestado_number = 0, $autoV = 0)
    {

        $value = $types2->getTypePrice();

        if($types2->getTypeId() == 25 || $types2->getTypeId() == 29){
           $value = $autoV;
        }



        $Total = 0;


        $Total += $Rasa = 5;
        $Total += $Selo = 10;
        $Total += $Imposto = ($value - (10)) * 0.1;
        $Total += $Emolumento = ($value - 10) - $Rasa - $Imposto;

        $Zero = $Emolumento + $Rasa;
        $Rasa = $Zero == 0 ? 0 : $Rasa;
        $Emolumento = $Zero == 0 ? 0 : $Emolumento;

        $Emolumento = number_format($Emolumento, 2);
        $Rasa = number_format($Rasa, 2);
        $Selo = number_format($Selo, 2);
        $Imposto = number_format($Imposto, 2);

        $F = new NumberFormatter("pt", NumberFormatter::SPELLOUT);
        $Extenso = ucfirst($F->format($Total));
        $Total = number_format($Total, 2);
        $StringHelper = new StringHelper();
        $string = strtoupper($StringHelper->separateString($type1->getDTypeName())) . " Nº. $atestado_number";

        $string = $this->setTracoCenter(CONTA-1, $string);
        ?>

        <?php


        return "
            <div class='conta'>
        <div  class='contas'>
        <table class='conta__table'>
            <tr class='conta__table__row'>
                <td class='conta__table__th text-center text-underline text-bold' style='text-align: center' colspan='2' >Conta</td>
            </tr>
            <tr class='conta__table__row'>
                <td class='conta__table__th'>Emolumentos</td>
                <td class='conta__table__th ctable__d--right'>$Emolumento dbs</td>
            </tr>
            <tr class='conta__table__row'>
                <td class='conta__table__th'>Imp Esp.</td>
                <td class='conta__table__th ctable__d--right'>$Imposto dbs</td>
            </tr>
            <tr class='conta__table__row'>
                <td class='conta__table__th'>Rasa</td>
                <td class='conta__table__th ctable__d--right'>$Rasa dbs</td>
            </tr>
            <tr class='conta__table__row'>
                <td class='conta__table__th'>Selo</td>
                <td class='conta__table__th ctable__d--right'>$Selo dbs</td>
            </tr>
            <tr class='conta__table__row'>
                <td class='conta__table__th text-bold'>Total</td>
                <td class='conta__table__th ctable__d--right text-bold'>$Total dbs</td>
            </tr>
            <tr class='conta__table__row'>
                <td class='conta__table__th text-center' style='text-align: center' colspan='2'>($Extenso dobras)</td>
            </tr>
        </table>
        </div>
        </div>
        <div class='clear'>
        </div>
<br>
    <p class='tittle text-center'>
     $string
              </p>


        ";
    }


    private function setTracoCenter($ct, $string)
    {


        $c = intval(($ct - strlen($string)) / 2);

        $newString = "";


        for ($i = 0; $i < $c; $i++) {
            $newString .= "-";
        }
        $newString .= $string;

        for ($i = 0; $i < $c; $i++) {
            $newString .= "-";
        }
        return $newString;

    }


    private function setTracoLast($ct, $string)
    {


        $c = intval(($ct - strlen($string)));

        $newString = "------" . $string;


        for ($i = 0; $i < $c; $i++) {
            $newString .= "-";
        }


        return $newString;

    }

    private function footer()
    {
        return "
<br>

    <p class='p-center'>
    O Presidente
    <br>
    <br>
    <br>
Anahory Dias Abílio do Espirito</p>
    ";
    }

    private function presidente()
    {
        return "ANAHORY DIAS ABÍLIO DO ESPIRITO, PRESIDENTE DA CÂMARA DISTRITAL DE MÉ-ZÓCHI.";
    }

    private function textoFinal(DocumentTypes $type1, DocumentForm $form = null)
    {
        $text = "<br>------Por ser verdade e ter sido requerido, mandou passar o
        presente Atestado, que assina, sendo a sua assinatura autenticada com o carimbo em uso nesta Câmara.---------------------------
        ";
        if ($type1->getDTypeId() == 2) {
            $text = "<br>------Por ser verdade e ter sido requerido, mandou passar autorização,
          que vai assinada e autenticada com o carimbo em uso nesta Câmara.
          ------------------------------------------------------";

        }elseif ($type1->getDTypeId() == 3) {
            $text = "";

        }elseif ($type1->getDTypeId() == 4) {
            $text = "";
        }elseif ($type1->getDTypeId() == 5) {

        }elseif ($type1->getDTypeId() == 6) {
            //$form['atestado_date'] = sanitize(Date("Y")) . "-" . sanitize(Date("m")) . "-" . sanitize(Date("d"));

            $validade = new Dates(Date("d"),Date("m"), Date("Y")+1 );
            $text = "<br>
            ------Válida até " . $validade->getExtData() . ".-----------------------------------------

            ";
        }elseif ($type1->getDTypeId() == 7) {
            $text = "";
        }elseif ($type1->getDTypeId() == 8) {
            //$form['atestado_date'] = sanitize(Date("Y")) . "-" . sanitize(Date("m")) . "-" . sanitize(Date("d"));

            //$validade = new Dates(Date("d"),Date("m"), Date("Y")+1 );
            $text = "<br>
            ------Válida até " . $form->getData2()->getExtData() . ".-----------------------------------------
                <br>
                ------Às autoridades e mais a quem o conhecimento desta competir assim o tenham entendido.
        ------------------------------------------------------------------------------------------------------
            ";
        }





        return $text;


    }


    private function data($timestamp_date)
    {

        //dnd($timestamp_date);
        $data = new Dates();
        $data2 = $data->convertDateFromDataBase($timestamp_date);

        $data = $data2->getExtData();

        $string =
            "Câmara Distrital de Mé-Zóchi, na Cidade da Trindade, aos $data.";

        return $this->setTracoLast(DATA, $string);
    }

    /**
     * @return string
     */
    public function getPdfRoot()
    {
        return $this->pdf_root;
    }

    /**
     * @return string
     */
    public function getPdfName()
    {
        return $this->pdf_name;
    }

    /**
     * @return mixed
     */
    public function getPdfNumber()
    {
        return $this->pdf_number;
    }


}