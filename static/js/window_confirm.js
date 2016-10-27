function clicked() {
       if (confirm('Do you want to submit?')) {
           form.submit();
       } else {
           return false;
       }
    }
