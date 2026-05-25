
class Person
{
   private $name;
   private $genero_id;
   private $oa;
   private $nasc_data;

//$link = PROOT . "home/download/certidaos/" . $result->atestado_number . ".pdf" . "/". $this->view->type->type_id;
//$file = ROOT . DS . "files" . DS . "gerados" . DS . $type1 . DS . $type2 . DS . $nome;

    public function __construct($index, $form, $prefix = ''){
        $this->name = isset($form[$prefix . 'nome-2' . $index]) ? $form[$prefix . 'nome-2' . $index] : "";
        $this->genero_id = isset($form[$prefix . 'genero-2' . $index]) ? $form[$prefix . 'genero-2' . $index] : "";
        $oa = isset($form[$prefix . 'genero-2' . $index]) ? $form[$prefix . 'genero-2' . $index] : "";
        if($oa == 1){
            $this->oa = "o";
        }elseif($oa == 2){
            $this->oa = "a";
        }
        $this->nasc_data = new Dates(
           isset($form[$prefix . 'nas-dia' . $index]) ? $form[$prefix . 'nas-dia' . $index] : "",
            isset($form[$prefix . 'nas-mes' . $index]) ? $form[$prefix . 'nas-mes' . $index] : "",
            isset($form[$prefix . 'nas-ano' . $index]) ? $form[$prefix . 'nas-ano' . $index] : ""
        );
    }

    /**
     * @return string
     */
    public function getName()
    {
        return $this->name;
    }

    /**
     * @return string
     */
    public function getGeneroId()
    {
        return $this->genero_id;
    }

    /**
     * @return string
     */
    public function getOa()
    {
        return $this->oa;
    }

    /**
     * @return Dates
     */
    public function getNascData()
    {
        return $this->nasc_data;
    }








}