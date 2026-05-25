class Dates
{
    private $dia;
    private $mes;
    private $ano;
    private $data;

    private $ext_dia;
    private $ext_mes;
    private $ext_ano;
    private $ext_data;

    public function __construct($dia = '', $mes = '', $ano = '',$timestamp = null){
        $Dias = new Dias();
        $Meses = new Meses();
        $Anos = new Anos();
        if($timestamp != null){
            $dia = $this->GetFromStamp($timestamp,'d');
            $mes = $this->GetFromStamp($timestamp,'m');
            $ano = $this->GetFromStamp($timestamp,'Y');
        }


        $diaO = $Dias->getById(sanitize($dia));
        $mesO = $Meses->getById(sanitize($mes));
        //$anoO = $Anos->getById(sanitize($ano));
        //dnd($ano);

        $dia_v = $diaO->dia_name;
        $mes_v = $mesO->mes_id;
        $ano_v = $ano;

        $this->dia = $dia_v < 10 ? "0" . $dia_v : $dia_v;
        $this->mes = $mes_v < 10 ? "0" . $mes_v : $mes_v;
        $this->ano = $ano_v;

        $this->data = $this->dia . "/" . $this->mes . "/" . $this->ano;

        $this->ext_dia = NumeroEmExtenso($dia_v);
        $this->ext_mes = $mesO->mes_name;
        $this->ext_ano = NumeroEmExtenso($ano_v);

        $this->ext_data = $this->ext_dia . " de " . $this->ext_mes . " de " . $this->ext_ano;
    }

    public function GetFromStamp($stamp, $pos){


        $d = new DateTime($stamp);



        $time = $d->getTimestamp();

        if($time != null){
            //return(date("Y-m-d H:i:s",$time ));
            return(date($pos,$time ));

        }
        return $time;
    }



    public function convertDateFromDataBase($atestado_date){
        //$atestado_date = $atestado->atestado_date;
        return new $this(GetFromStamp($atestado_date, 'd'),GetFromStamp($atestado_date, 'm'),GetFromStamp($atestado_date, 'Y')  );
    }


    public static function display($timestamp){
        $date = new self("","","",$timestamp);
        return $date->getData();
    }

    public static function getDay($timestamp){
        $date = strtotime($timestamp);
        return date('j', $date);
    }

    public static function getMonth($timestamp){
        $date = strtotime($timestamp);
        return date('M', $date);
    }
    public static function getYear($timestamp){
        $date = strtotime($timestamp);
        return date('Y', $date);
    }


    /**
     * @return mixed
     */
    public function getDia()
    {
        return $this->dia;
    }

    /**
     * @return mixed
     */
    public function getMes()
    {
        return $this->mes;
    }

    /**
     * @return mixed
     */
    public function getAno()
    {
        return $this->ano;
    }

    /**
     * @return mixed
     */
    public function getData()
    {
        return $this->data;
    }

    /**
     * @return string
     */
    public function getExtDia()
    {
        return $this->ext_dia;
    }

    /**
     * @return string
     */
    public function getExtMes()
    {
        return $this->ext_mes;
    }

    /**
     * @return string
     */
    public function getExtAno()
    {
        return $this->ext_ano;
    }

    /**
     * @return mixed
     */
    public function getExtData()
    {
        return $this->ext_data;
    }





}