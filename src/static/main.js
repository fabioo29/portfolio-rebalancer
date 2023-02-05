jQuery(document).ready(function () {
    // Add asset button click event
    $("#addAssetBtn").click(function () {
        $("#assetsTableBody").append('<tr><td><input type="text" class="form-control" placeholder="Ticker"/></td><td><input type="number" class="form-control" placeholder="Current Value"/></td><td><input type="number" class="form-control" placeholder="Target Allocation"/></td><td><button type="button" class="btn btn-danger delete-btn">Delete</button></td></tr>');
    });
    // Delete asset button click event
    $("#assetsTableBody").on("click", ".delete-btn", function () {
        $(this).parents("tr").remove();
    });

    // Rebalance button click event
    $("#rebalanceBtn").click(function () {
        var cash = $("#cashInput").val();
        var assets = {};
        var target_asset_alloc = {};
        $("#assetsTableBody tr").each(function () {
            var ticker = $(this).find("td").eq(0).find("input").val();
            var current_value = $(this).find("td").eq(1).find("input").val();
            var target_alloc = $(this).find("td").eq(2).find("input").val();
            assets[ticker] = current_value;
            target_asset_alloc[ticker] = target_alloc;
        });

        $.ajax({
            url: "/rebalance",
            type: "POST",
            data: JSON.stringify({
                cash: cash,
                assets: assets,
                target_asset_alloc: target_asset_alloc
            }),
            contentType: "application/json",
            success: function (data) {
                console.log(data);
                if (data) {
                    for (var i = 0; i < data.length; i++) {
                        console.log(data[i]);
                        var ticker = data[i].ticker;
                        var investing = data[i].to_buy_val;
                        var total_asset_value = data[i].new_asset_amount;
                        var prev_asset_alloc = data[i].prev_asset_alloc;
                        var target_allocation = data[i].target_alloc;
                        var new_allocation = data[i].new_alloc;
                        var difference = data[i].alloc_diff;
                        $("#resultsTableBody").append('<tr><td>' + ticker + '</td><td>' + investing + ' $</td><td>' + total_asset_value + ' $</td><td>' + prev_asset_alloc + ' %</td><td>' + target_allocation + ' %</td><td>' + new_allocation + ' %</td><td>' + difference + ' %</td></tr>');
                    }
                    $("#resultsTableBody").append('<tr><td colspan="7"><hr></td></tr>');
                }
            },
            error: function (error) {
                //console.log('');
            }
        });
    });

    // Clear button click event
    $("#clearBtn").click(function () {
        $("#resultsTableBody").empty();
    });

    // whenever the user changes the value of the placeholder="Target Allocation" input calculate the sum of all the values
    // in that col and change the header title of the col to "Target Allocation (sum)"
    $("#assetsTableBody").on("change", "input", function () {
        var sum = 0;
        $("#assetsTableBody tr").each(function () {
            var target_alloc = $(this).find("td").eq(2).find("input").val();
            if (target_alloc) {
                sum += parseInt(target_alloc);
            }
        });
        $(".table tr th").eq(2).text("Target Allocation (" + sum + "%)");
    });
});