frappe.ui.form.on("Resource Utilisation", {

    refresh(frm) {
        frm.add_custom_button(
            "View Report",
            function () {

                if (!frm.doc.from_date || !frm.doc.to_date) {
                    frappe.msgprint(
                        "Please set From Time and To Time!"
                    );
                    return;
                }

                if (frm.doc.from_date > frm.doc.to_date) {
                    frappe.msgprint(
                        "From Time must be less than To Time!"
                    );
                    return;
                }

                // ✅ Directly open print page
                window.open(
                    frappe.urllib.get_full_url(
                        `/printview?`
                        + `doctype=Resource Utilisation`
                        + `&name=Resource Utilisation`
                        + `&format=Resource Utilisation`
                        + `&no_letterhead=0`
                        + `&letterhead=No Letterhead`
                        + `&settings={}`
                        + `&_lang=en`
                    ),
                    "_blank"
                );
            }
        );
    }

});