module Types exposing (..)

type alias Person =
    { name : String
    , age : Int
    , address : List Address
    , names : List String
    , paypal_email : Maybe String
    }
type alias Address =
    { street : String
    , number : Int
    }
