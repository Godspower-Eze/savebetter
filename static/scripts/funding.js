function decToHex (dec) {
    return dec.toString(16).padStart(2, "0")
}

function generateReference(){
    var arr = new Uint8Array(40 / 2)
    window.crypto.getRandomValues(arr)
    return Array.from(arr, decToHex).join('')
}

document.addEventListener('DOMContentLoaded',()=>{

    SendcashPay.init({
        siteName: "Save Better",
        siteUrl: "http://codingwithease.com/",
        siteLogo: "https://codingwithease.com/wp-content/uploads/2020/10/CWE-HEADER..png",
        publicKey: "pk_live_VbmBSJcYHTDIMPxHUKnwydRhVsvROVDQ"
    })

    const fundForm = document.getElementById("funding-form")
    
    fundForm.addEventListener('submit', event => {

        event.preventDefault()
        let numberField = document.getElementById("funding-form-number-field")
        let amount = parseInt(numberField.value)
        numberField.value = ""

        let userId = fundForm.getAttribute("data-username")
        let reference = generateReference()
        let amount_in_kobo = amount * 100

        let url = `${window.location.protocol}//${window.location.host}/generate_signature/`

        $.ajax({
            url:url,
            type:'POST',
            data:{
              'user_id': userId,
              'reference': reference,
              'amount_in_kobo':amount_in_kobo,
              'csrfmiddlewaretoken': fundForm.children[0].value
            },
            success:function(resp){
                signature = resp.signature
                const result = SendcashPay.chargeToDefaultAccount({
                    signature: signature,
                    amount: amount,
                    userId: userId,
                    transactionReference: reference
                })
            }
      })
    })

})