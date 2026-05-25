
class BiDetails (StringHelper)
{


    public function __construct($bi_id){
        Bis::getById(sanitize($bi_id));




    }

}