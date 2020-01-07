module Utils exposing (PosixZone, jpFromDayOfWeek, localDateTime, monthFromInt, parseDate, strFromDayOfWeek)

import Calendar
import DateTime
import Time exposing (Month(..), Posix, Weekday(..))



-- boring stuff.
-- like months from ints and stuff.


type alias PosixZone =
    { posix : Time.Posix
    , zone : Time.Zone
    }



-- Parse "2019/11/21" into a Maybe Calendar.Date


parseDate : String -> Maybe Calendar.Date
parseDate date =
    let
        parts =
            String.split "/" date
    in
    case parts of
        [ yearStr, monthNumStr, dayStr ] ->
            let
                maybeMonth =
                    monthFromInt (String.toInt monthNumStr)

                maybeDay =
                    String.toInt dayStr

                maybeYear =
                    String.toInt yearStr
            in
            case ( maybeYear, maybeMonth, maybeDay ) of
                ( Just year, Just month, Just day ) ->
                    Calendar.fromRawParts { day = day, month = month, year = year }

                _ ->
                    Nothing

        _ ->
            Nothing


localDateTime posix zone =
    let
        offset =
            DateTime.getTimezoneOffset zone posix
    in
    DateTime.fromPosix
        (Time.millisToPosix
            (Time.posixToMillis posix + offset)
        )


monthFromInt : Maybe Int -> Maybe Month
monthFromInt maybeMonthNum =
    case maybeMonthNum of
        Nothing ->
            Nothing

        Just monthNum ->
            case monthNum of
                1 ->
                    Just Jan

                2 ->
                    Just Feb

                3 ->
                    Just Mar

                4 ->
                    Just Apr

                5 ->
                    Just May

                6 ->
                    Just Jun

                7 ->
                    Just Jul

                8 ->
                    Just Aug

                9 ->
                    Just Sep

                10 ->
                    Just Oct

                11 ->
                    Just Nov

                12 ->
                    Just Dec

                _ ->
                    Nothing


strFromDayOfWeek day =
    case day of
        Mon ->
            "mon"

        Tue ->
            "tue"

        Wed ->
            "wed"

        Thu ->
            "thu"

        Fri ->
            "fri"

        Sat ->
            "sat"

        Sun ->
            "sun"


jpFromDayOfWeek day =
    case day of
        Mon ->
            "月"

        Tue ->
            "火"

        Wed ->
            "水"

        Thu ->
            "木"

        Fri ->
            "金"

        Sat ->
            "土"

        Sun ->
            "日"
