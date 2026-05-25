



        $fim = "Efeitos de ";


        $espaco = "&nbsp;";
        $terminais = ['o','a', 'os', 'as'];
        //dnd($this->getForm()->getCompanheiros());
        $companheiro_text   = $this->getDetails($this->getForm()->getCompanheiros(), 'companheir',$terminais);

        $filho_text       = $this->getDetails($this->getForm()->getFilho(), 'filh',$terminais);
        $primos_text         = $this->getDetails($this->getForm()->getPrimo(), 'prim',$terminais);
        $sobrinho_text     = $this->getDetails($this->getForm()->getSobrinho(), 'sobrinh',$terminais);
        $entiado_text       = $this->getDetails($this->getForm()->getEntiado(), 'entiad',$terminais);
        $sogros_text       = $this->getDetails($this->getForm()->getSogro(), 'sogr',$terminais);
        $neto_text   = $this->getDetails($this->getForm()->getNeto(), 'net',$terminais);
        $afilhado_text   = $this->getDetails($this->getForm()->getAfilhado(), 'afilhad',$terminais);
        $tios_text   = $this->getDetails($this->getForm()->getTio(), 'ti',$terminais);
        $cunhados_text   = $this->getDetails($this->getForm()->getCunhado(), 'cunhad',$terminais);

        $terminais = ['ô','ó', 'ôs', 'ós'];
        $avo_text = $this->getDetails($this->getForm()->getAvos(), 'av',$terminais);

        $terminais = ['o','', 'os', 's'];
        $irmaos_text = $this->getDetails($this->getForm()->getIrmao(), 'irmã',$terminais);

        $atestado_desde = " há mais de " . NumeroEmExtenso($this->getForm()->getDesde()) . " ano";

        $atestado_desde .= $this->getForm()->getDesde() == 1 ? "":"s";




        $bemcomo = $neto_text . $sobrinho_text . $entiado_text . $afilhado_text .
            $tios_text . $primos_text . $sogros_text . $irmaos_text . $cunhados_text;


        $bemcomo = $bemcomo == "" ? "" : " bem como " . $rest = substr($bemcomo, 1);

        $pai_text = "";
        //dnd($this->getForm());
        if($this->getForm()->getPai() == 1){
            $pai_text = $this->getPai($this->getForm()->getPai1(1));

        }
        $mae_text = "";
        if($this->getForm()->getMae() == 1){
            $mae_text = $this->getMae($this->getForm()->getMae1(1));
        }
        $reside = "residente efetivamente";
        $vive = "vive em comunhão de mesa e a";
       
        if($this->getForm()->getCountry()->getCountryName() != null){
            $reside = "residiu";
             $vive = "atualmente á residir em " . $this->getForm()->getCountry()->getCountryName() . ", tem ao";
        }


        $this->text = "Atesta para " . $fim .  $this->getType2()->getTypeName() 
            ." que ".
            StringHelper::getTextBi($this->getBi1(), $this->getBi2(),$this->getType2()->getTypeId())
            . " " . $reside . $this->getForm()->getHouseExt() .
            " na localidade de ". $this->getForm()->getLocalidade()->getLocalidadeName() . ", Distrito de Mé-Zóchi, deste Estado,
            " . $vive. " seu
            exclusivo cargo,$espaco $companheiro_text $pai_text $mae_text $avo_text
     $filho_text $bemcomo $atestado_desde.";



        return new PDF($this->text,$this->getType(),$this->getType2(), $this->getGerados());
    }


    private function getDetails($params, $next_name, $terminais)
    {


        // $params, = array do tio, cunhado...
        //$total, = qtd do item no params
        // $next_name = iniciais , ti, cunhad...

        //dnd($params);
        if($params == null){
            return "";
        }
        $primeiro = false;
        if ($this->getForm()->getTotal() == 1) {
            $primeiro = true;
        }

        //dnd($params);
        $total = count($params);
        $text = "";
        if (count($params) == 0) {
            return $text;
        } elseif ($total == 1 && $primeiro == false ||  $primeiro == true) {
            $text = $params[1]->getGeneroId() == 1 ? " seu " . $next_name . $terminais[0] ."," : " sua " . $next_name . $terminais[1] . "";
        }  elseif ($total > 1) {
            $text = " suas " . $next_name . $terminais[3]. "";
            for ($i = 1; $i <= $total; $i++) {
                if ($params[$i]->getGeneroId() == 1) {
                    $text = " seus " . $next_name. $terminais[2] . "";
                }
            }
        }

        for ($i = 1; $i <= $total; $i++) {

            $text .= " " . toBold($params[$i]->getName()) . ", nascid" . $params[$i]->getOa() . " em " .$params[$i]->getNascData()->getExtData(). ",";

        }
        return $text;

    }

    private function getPai($params)
    {
        if($params == null){
            return "";
        }

        $text = " seu pai,";

        $text .= " " . toBold($params->getName()) . ", nascido em " .
            $params->getNascData()->getExtData() . ",";
        return $text;

    }

    private function getMae($params)
    {
        if($params == null){
            return "";
        }
        $text = " sua mãe,";

        $text .= " " . toBold($params->getName()) . ", nascida em " .
            $params->getNascData()->getExtData(). ",";
        return $text;

    }



    /**
     * @return mixed
     */
    public function getText()
    {
        return $this->text;
    }



    function store()
    {
        $this->storeInDB($this);

        // TODO: Implement create() method.
        dnd($this);

    }

    function read()
    {
        // TODO: Implement read() method.
    }

    function aproveFirst()
    {
        // TODO: Implement aproveFirst() method.
    }

    function aproveSecond()
    {
        // TODO: Implement aproveSecond() method.
    }

}