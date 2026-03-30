/*frappe.listview_settings["Resource"] = {
    onload(listview) {
        listview.page.add_inner_button(
            "Resource Utilisation Report",
            function () {
                let dialog = new frappe.ui.Dialog({
                    title:  "Resource Utilisation Report",
                    fields: [
                        {
                            fieldname: "from_date",
                            fieldtype: "Date",
                            label:     "From Date",
                            reqd:      1,
                        },
                        {
                            fieldname: "to_date",
                            fieldtype: "Date",
                            label:     "To Date",
                            reqd:      1,
                        },
                    ],
                    primary_action_label: "Download PDF",
                    primary_action(values) {
                        if (values.from_date > values.to_date) {
                            frappe.msgprint("From Date must be less than To Date");
                            return;
                        }
                        window.open(
                            frappe.urllib.get_full_url(
                                `/api/method/event_scheduler.event_scheduler.doctype.resource.resource.get_resource_utilisation_pdf`
                                + `?from_date=${values.from_date}`
                                + `&to_date=${values.to_date}`
                            ),
                            "_blank"
                        );
                        dialog.hide();
                    }
                });
                dialog.set_value("from_date", frappe.datetime.month_start());
                dialog.set_value("to_date",   frappe.datetime.month_end());
                dialog.show();
            }
        );
    }
};*/

