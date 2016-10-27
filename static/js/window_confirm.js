function clicked() {
       if (alert('Inserimento effettuato con successo.')) {
           form.submit();
       } else {
           return false;
       }
    }
    
function clicked_check() {
       if (confirm('Sicuro di voler procedere ?')) {
           form.submit();
       } else {
           return false;
       }
    }
    
