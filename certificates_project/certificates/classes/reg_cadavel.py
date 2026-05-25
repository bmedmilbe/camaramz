
class RegCadavel (DocumentData) implements Document
{
    private $text;
    function create()

    {
        // TODO: Implement create() method.




$tempo = "";

        $this->text = "Deu entrada no Cemitério da ". $this->getForm()->getCemiterio()->getDistritoName().", Distrito de Mé-Zóchi
         o caixão e o cadavél de nome ".
            StringHelper::getTextBi($this->getBi1(), $this->getBi2(),$this->getType2()->getTypeId(), $this->getForm())
            ."

         Domestica, falecid".$this->getBi1()->getBiOa()." em " . $this->getForm()->getLocalidade()->getLocalidadeFull() .
            ", em " . $this->getForm()->getData1()->getExtData(). "

         sepultad" .$this->getBi1()->getBiOa()." pelas 16 horas 30 minutos,
         em " . $this->getForm()->getData2()->getExtData() . ",
         no coval número " . $this->getForm()->getCovalName() . " do
    ano " . $this->getForm()->getAnoName() . ",
          o mesmo coval foi requerido para ser comprado pel" .  $this->getForm()->getOa1() ."

          senhor" . $this->getForm()->getOa1() ." ". toBold($this->getForm()->getNome1()) ." em ".
            " ". $this->getForm()->getData4()->getExtData() ."
           e foi comprado pel".$this->getForm()->getOa21()." senhor" .  $this->getForm()->getOa2() . " " .
            toBold($this->getForm()->getNome2()) ." em ".
            " ". $this->getForm()->getData5()->getExtData() .".

           No mesmo coval foi enterrad" .  $this->getForm()->getOa31() . " senhor" .$this->getForm()->getOa3(). "
            ". toBold($this->getForm()->getNome3()) ." em ".
            " ". $this->getForm()->getData6()->getExtData() .". <br>
Causa da Morte: ".$this->getForm()->getCausa().".";

        return new RegPDF($this->text,$this->getType(),$this->getType2(), $this->getGerados(), $this->getForm());
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