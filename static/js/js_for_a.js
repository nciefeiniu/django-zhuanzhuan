$(document).ready(function () {
        $("a#list_login").mouseover(
            function () {
                $(this).css("color", "#ff0000");
            }
        )

        $("a#list_login").mouseout(
            function () {
                $(this).css("color", "#666");
            }
        )

        $("span.right-selection").find("a").mouseover(
            function () {
                $(this).css({"color": "#ff0000", "font-weight": "700"});
            }
        )

         $("span.right-selection").find("a").mouseout(
            function () {
                $(this).css({"color": "#a6a6a6", "font-weight": "100"});
            }
        )
    }
)
