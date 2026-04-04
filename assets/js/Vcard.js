    function generateVCard() {
      const vcard = "BEGIN:VCARD\n" +
                    "VERSION:3.0\n" +
                    "FN:Grégory Loubet-Bonino\n" +
                    "ORG:University of Bern - SEG Group\n" +
                    "TITLE:PhD Student in Software Engineering\n" +
                    "EMAIL;TYPE=INTERNET:gregory.loubet-bonino@unibe.ch\n" +
                    "URL:https://dragonfuneste.github.io\n" +
                    "ADR:;;Bern;Switzerland;;\n" +
                    "END:VCARD";
      
      const blob = new Blob([vcard], { type: "text/vcard" });
      const url = window.URL.createObjectURL(blob);
      const newLink = document.createElement("a");
      newLink.href = url;
      newLink.setAttribute("download", "Gregory_Loubet_Bonino.vcf");
      newLink.click();
    }