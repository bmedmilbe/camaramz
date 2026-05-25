
class LicBarraca (DocumentData) implements Document
{
    private $text;
    function create()

    {
        // TODO: Implement create() method.




$tempo = "";




        $this->text = "Por esta Câmara se faz constar as
         autoridades e mais pessoas a quem o conhecimento
         desta competir que foi concedida
Autorização " . $this->getBi1()->getBiOa3() . " senhor" .$this->getBi1()->getBiOa2() . " " .
            StringHelper::getTextBi($this->getBi1(), $this->getBi2(),$this->getType2()->getTypeId(), $this->getForm())
            . " residente em " . $this->getForm()->getLocalidade()->getLocalidadeFull() .
            " para proceder o funcionamento de " . $this->getForm()->getObjecto() . ",
            na localidade de ". $this->getForm()->getLocalidade1()->getLocalidadeFull() .".";

        return new PDF($this->text,$this->getType(),$this->getType2(), $this->getGerados(), $this->getForm());
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