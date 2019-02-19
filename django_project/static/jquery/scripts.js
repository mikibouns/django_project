jQuery(document).ready(function() {
 // маска для номера телефона
 $('#phone').mask('+#(###)###-##-##', {placeholder: "+_(___)___-__-__"});
 // маска для email
 $('#email').mask("A", {translation: {'A': {pattern: /[\w@\-.+]/, recursive: true}}, placeholder: "___@___.__"});

 $("#another_pms").hide();
 $('label[for="another_pms"]').hide();
 $('#pms').change(function() {
  if($(this).val() === "another")
   {
    $("#another_pms").show();
    $('label[for="another_pms"]').show();
   }
   else
   {
    $("#another_pms").hide();
    $('label[for="another_pms"]').hide();
   }
 });
});