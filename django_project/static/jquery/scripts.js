$(document).ready(function() {
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
  $('#phone').mask("+9(999)999-99-99");
//  $('#email').mask("A", {
//	translation: {
//		"A": { pattern: /[\w@\-.+]/, recursive: true }
//	}
//  });
});