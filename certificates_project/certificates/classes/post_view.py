
//include 'vendor/autoload.php';

require_once("files/PHPWord/vendor/autoload.php");

class PostView extends ExtractWords
{
    private $frame_count;
    public $frame;
    private $text;
    private $file;
    private $route;
    private $charater;
    private $parts;

    public function __construct($route, $file, $frames =  [])
    {


        $this->route = ROOT . DS . "files" . DS . $route . DS;

        $this->frame_count = 0;
        $this->file = str_getcsv($file, ".")[0];
        $this->readDocx3();

        foreach ($frames as $frame):
            //var_dump($frames);
            $this->setFrame($frame->frame_name);
        endforeach;

        $this->parts = $this->render();


        parent::__construct($this->getRoute() . $file);

        $this->charater = $this->convertToText();

    }


    function readDocx4()
    {

        $phpWord = \PhpOffice\PhpWord\IOFactory::load('ola.html', 'HTML');
        $wordWriter = new \PhpOffice\PhpWord\Writer\Word2007($phpWord);

        $wordWriter->save('ola2.docx');
        //$htmlWriter->save('ola.html');
    }

//FUNCTION :: read a docx file and return the string
    function readCharacters($filePath)
    {
        $docObj = new ExtractWords($filePath);

        return $docObj->convertToText();

    }


    function readDocx2($filePath)
    {
        // Create new ZIP archive
        $zip = new ZipArchive;
        $dataFile = 'word/document.xml';
        // Open received archive file
        if (true === $zip->open($filePath)) {
            // If done, search for the data file in the archive
            if (($index = $zip->locateName($dataFile)) !== false) {
                // If found, read it to the string
                $data = $zip->getFromIndex($index);
                // Close archive file
                $zip->close();
                // Load XML from a string
                // Skip errors and warnings
                $xml = new DOMDocument("1.0", "utf-8");
                $xml->loadXML($data, LIBXML_NOENT | LIBXML_XINCLUDE | LIBXML_NOERROR | LIBXML_NOWARNING | LIBXML_PARSEHUGE);
                $xml->encoding = "utf-8";
                // Return data without XML formatting tags
                $output = $xml->saveXML();
                $output = str_replace("w:", "", $output);

                return $output;
            }
            $zip->close();
        }
        // In case of failure return empty string
        return "";
    }


//Transform in html
    function readDocx3()
    {
        //dnd($this->getRoute() . $this->getFile().".docx");


        $phpWord = \PhpOffice\PhpWord\IOFactory::load($this->getRoute() . $this->getFile() . ".docx"); // .docx
        $htmlWriter = new \PhpOffice\PhpWord\Writer\HTML($phpWord);
        $htmlWriter->save($this->getRoute() . $this->getFile() . '.html');
    }

    /**
     * @return mixed
     */
    public function getFrameCount()
    {
        return $this->frame_count;
    }


    public function getFile()
    {
        return $this->file;
    }

    public function getRoute()
    {
        return $this->route;
    }

    public function getCharater()
    {

        $chars = str_getcsv($this->charater, "@");
        if ($chars) {
            $text = "";
            foreach ($chars as $char):
                $text .= $char;
            endforeach;
        }
        return $text;
    }

    /**
     * @param mixed $frame_count
     */

    /**
     * @return mixed
     */
    public function getFrame($index)
    {
        return $this->frame[$index];
    }

    public function getParts()
    {
        return $this->parts;
    }

    /**
     * @param mixed $frame
     */
    public function setFrame($frame)
    {
        $this->frame[$this->frame_count] = $frame;
        $this->frame_count++;
    }

    /**
     * @return mixed
     */
    public function getText()
    {
        return $this->text;
    }






    /**
     * @param mixed $text
     */
    public function render()
    {

//Divid HTML By @
        $results = str_getcsv(file_get_contents($this->getRoute() . $this->getFile() . '.html'), "@");

//var_dump($results);
        $contF = 0;
//Show text
        $new = array();
        $count = 0;

        foreach ($results as $key => $result):
            $new[$count++] = $result . '<br>';
            $this->text .= $result . '<br>';
            if ($this->getFrameCount() > $contF):
                 $this->text .= '<div
            style="max-width: 700px;margin: 0 auto"
                     class="embed-responsive embed-responsive-16by9">'.$this->getFrame($contF) . '</div><br>';
                $new[$count++] = $this->getFrame($contF) . '<br>';

            endif;
            $contF++;
        endforeach;
        $this->text = get_string_between($this->text, '<body>', '<body>');
        return  $new;

    }

}


//Transform in html
//readDocx3();

//Insert fames by index


?>
<?php
//$newhtml = str_replace("@", $frame, file_get_contents('ola.html'));


?>
