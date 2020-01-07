module Main exposing (main)

import Browser
import Browser.Dom
import Calendar
import DateTime
import Html exposing (Html, div, h1, h2, h3, p, span, text)
import Html.Attributes exposing (class)
import Html.Events exposing (onClick)
import Http
import Json.Decode exposing (Decoder, bool, field, list, string)
import Parser exposing ((|.), (|=))
import Task
import Time exposing (Month(..), Posix, Weekday(..))
import Utils exposing (..)


schedule_url =
    "/schedule"


getRequest =
    Http.get
        { url = schedule_url
        , expect = Http.expectJson GotEvents scheduleDecoder
        }


main =
    Browser.element
        { init = init
        , view = view
        , update = update
        , subscriptions = subscriptions
        }


type Model
    = LoadingModel
    | ErrorModel String
    | EventModelNoDate (List DaySchedule)
    | EventModelWithDate (List DaySchedule) DateTime.DateTime


init : () -> ( Model, Cmd Msg )
init _ =
    ( LoadingModel
    , getRequest
    )


itemsDecoder : Decoder (List Event)
itemsDecoder =
    list (Json.Decode.map5 Event (field "info" string) (field "from_time" string) (field "to_time" string) (field "flag" bool) (field "location" string))


dayScheduleDecoder : Decoder DaySchedule
dayScheduleDecoder =
    Json.Decode.map2 DaySchedule (field "date" string) (field "events" itemsDecoder)


scheduleDecoder : Decoder (List DaySchedule)
scheduleDecoder =
    list
        dayScheduleDecoder


type Msg
    = GotEvents (Result Http.Error (List DaySchedule))
    | ReceiveDate PosixZone
    | Update
    | ScrollNoOp
    | Rescroll


type alias Event =
    { info : String
    , from_time : String
    , to_time : String
    , flag : Bool
    , location : String
    }


type alias DaySchedule =
    { date : String
    , events : List Event
    }


makeEvent str =
    Event str


renderBreaksAndEvents : List (Html Msg) -> Maybe Event -> List Event -> List (Html Msg)
renderBreaksAndEvents listSoFar maybePrevious eventsToRender =
    case eventsToRender of
        [] ->
            listSoFar

        head :: tail ->
            let
                rendered =
                    case maybePrevious of
                        Nothing ->
                            [ renderEvent head ]

                        Just previous ->
                            renderBreakAndEvent previous head
            in
            renderBreaksAndEvents (listSoFar ++ rendered) (Just head) tail


renderEvents : List Event -> List (Html Msg)
renderEvents events =
    renderBreaksAndEvents [] Nothing events



--    List.map renderEvent events


renderBreak : Event -> Event -> List (Html Msg)
renderBreak prev next =
    let
        intWithZeros =
            Parser.map (Maybe.withDefault 0)
                (Parser.succeed String.toInt
                    |= Parser.getChompedString (Parser.chompWhile Char.isDigit)
                )

        timeParser =
            Parser.succeed Tuple.pair
                |= intWithZeros
                |. Parser.symbol ":"
                |= intWithZeros
                |. Parser.end

        from_result =
            Parser.run timeParser prev.to_time

        to_result =
            Parser.run timeParser next.from_time

        interval =
            prev.to_time ++ " -> " ++ next.from_time
    in
    case ( from_result, to_result ) of
        ( Ok from, Ok to ) ->
            let
                ( from_h, from_m ) =
                    from

                ( to_h, to_m ) =
                    to

                diff_h_part =
                    to_h - from_h

                diff_m_part =
                    to_m - from_m

                diff_m_total =
                    diff_h_part * 60 + diff_m_part

                diff_m =
                    modBy 60 diff_m_total

                diff_h =
                    diff_m_total // 60

                h_str =
                    case diff_h of
                        0 ->
                            ""

                        hours ->
                            String.fromInt diff_h ++ "h"

                m_str =
                    case diff_m of
                        0 ->
                            ""

                        mins ->
                            String.fromInt diff_m ++ "m "

                classes =
                    [ class "break" ]
                        ++ (if diff_m_total > 15 then
                                [ class "break-long" ]

                            else
                                []
                           )
            in
            if diff_h >= 0 && diff_m >= 0 then
                [ span classes [ text (h_str ++ m_str ++ "break.") ] ]

            else
                []

        _ ->
            []


renderBreakAndEvent : Event -> Event -> List (Html Msg)
renderBreakAndEvent prev next =
    renderBreak prev next ++ [ renderEvent next ]


renderEvent : Event -> Html Msg
renderEvent item =
    let
        maybeflag =
            case item.flag of
                True ->
                    [ class "flag" ]

                False ->
                    []
    in
    div maybeflag [ span [ class "time" ] [ text (item.from_time ++ " - " ++ item.to_time) ], span [ class "location" ] [ text ("@" ++ item.location) ], p [] [ text item.info ] ]


formatDate : Calendar.Date -> Bool -> String
formatDate dt withWeekday =
    let
        dayStr =
            String.padLeft 2 '0' (String.fromInt (Calendar.getDay dt))

        monthStr =
            String.padLeft 2 '0' (String.fromInt (Calendar.monthToInt (Calendar.getMonth dt)))

        yearStr =
            String.padLeft 4 '0' (String.fromInt (Calendar.getYear dt))

        dayOfWeek =
            jpFromDayOfWeek (Calendar.getWeekday dt)
    in
    yearStr
        ++ "/"
        ++ monthStr
        ++ "/"
        ++ dayStr
        ++ (case withWeekday of
                True ->
                    " " ++ "(" ++ dayOfWeek ++ ")"

                False ->
                    ""
           )



renderDay : Maybe DateTime.DateTime -> DaySchedule -> Html Msg
renderDay maybedatetime day =
    let
        parsedDate =
            parseDate day.date

        parsedDateStr =
            case parsedDate of
                Just datetime ->
                    formatDate datetime True

                Nothing ->
                    day.date

        datestr =
            case maybedatetime of
                Just datetime ->
                    formatDate (DateTime.getDate datetime) False

                Nothing ->
                    ""

        isToday =
            case maybedatetime of
                Just today ->
                    case parsedDate of
                        Just eventdate ->
                            eventdate == DateTime.getDate today

                        Nothing ->
                            -- this is sooo ugly but kinda works
                            day.date == datestr

                Nothing ->
                    False

        isWeekend =
            case parsedDate of
                Just eventdate ->
                    case Calendar.getWeekday eventdate of
                        Sat ->
                            True

                        Sun ->
                            True

                        _ ->
                            False

                Nothing ->
                    False

        maybeToday =
            if isToday then
                [ class "today", Html.Attributes.id "today" ]

            else
                []

        maybeWeekend =
            if isWeekend then
                [ class "weekend" ]

            else
                []

        extraClasses =
            maybeToday ++ maybeWeekend

        events =
            renderEvents day.events

        datestring =
            if isToday then
                "today"

            else
                "on " ++ day.date

        numEvents =
            List.length day.events

        summary =
            case day.events of
                [] ->
                    "No events " ++ datestring ++ "!"

                some_events ->
                    "You have "
                        ++ String.fromInt numEvents
                        ++ (if numEvents == 1 then
                                " event "

                            else
                                " events "
                           )
                        ++ datestring
                        ++ "."
    in
    div ([ class "day" ] ++ extraClasses)
        ([ h3 [ class "date" ] [ text parsedDateStr ]
         , span [ class "summary" ] [ text summary ]
         ]
            ++ events
        )


view : Model -> Html Msg
view model =
    case model of
        LoadingModel ->
            Html.div []
                [ Html.h1 [] [ text "Loading your plan..." ]
                , Html.p [] [ text "(waiting for loyola to give us your schedule)" ]
                ]

        ErrorModel error ->
            Html.p [] [ text ("Ouch! something didn't work: " ++ error) ]

        EventModelNoDate days ->
            Html.div [] (List.map (renderDay Nothing) days)

        EventModelWithDate days time ->
            let
                todaysDate =
                    String.fromInt (DateTime.getDay time)
            in
            Html.div [] (List.map (renderDay (Just time)) days ++ [ Html.a [ onClick Rescroll, Html.Attributes.id "scrollbutton" ] [ text todaysDate ] ])


errorToString error =
    case error of
        Http.BadBody string ->
            "Did not understand response from Loyola or schedule loader: " ++ string

        Http.NetworkError ->
            "network error"

        _ ->
            "unknown error"


refreshDateTask =
    Task.perform ReceiveDate (Task.map2 PosixZone Time.now Time.here)


scrollTask =
    Browser.Dom.getElement "today" |> Task.andThen (\today -> Browser.Dom.setViewport 0 (today.element.y - 20)) |> Task.attempt (\_ -> ScrollNoOp)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        GotEvents res ->
            case res of
                Ok vals ->
                    ( EventModelNoDate vals, refreshDateTask )

                Err info ->
                    ( ErrorModel (errorToString info), Cmd.none )

        ReceiveDate posixzone ->
            let
                days =
                    case model of
                        EventModelNoDate events ->
                            events

                        EventModelWithDate events date ->
                            events

                        LoadingModel ->
                            []

                        ErrorModel _ ->
                            []

                posix =
                    posixzone.posix

                zone =
                    posixzone.zone
            in
            ( EventModelWithDate days
                (localDateTime
                    posix
                    zone
                )
            , scrollTask
            )

        Rescroll ->
            ( model, refreshDateTask )

        Update ->
            ( LoadingModel
            , getRequest
            )

        ScrollNoOp ->
            ( model, Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions _ =
    Sub.none
