module Types exposing (..)

type alias Person =
    { name : String
    , age : Int
    , address : Address
    }
type alias Address =
    { street : String
    , number : Int
    }
