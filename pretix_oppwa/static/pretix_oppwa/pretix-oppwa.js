$(function () {
    wpwlOptions = {
        locale: $.trim($("body").attr("data-locale")),
        googlePay: {
            gatewayMerchantId: $.trim($("#googlepay_gatewayMerchantId").html()),
            merchantId: $.trim($("#googlepay_merchantId").html()),
        }
    }
});
