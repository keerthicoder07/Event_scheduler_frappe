frappe.ui.form.on('Events', {

    refresh(frm) {
        format_datetime_fields(frm);

        frappe.realtime.on("event_auto_cancelled",function(data)
        {
            frappe.show_alert(
                {
                    message:data.message,
                    indicator:"orange"
                },7
                
            );
            frm.reload_doc();
        }
    );
    },

    onload_post_render(frm) {
        format_datetime_fields(frm);
    },

    start_time(frm) {
        format_datetime_fields(frm);
    },

    total_hours(frm) {
        calculate_end_time(frm);
    },

});

function calculate_end_time(frm)
{
    if(frm.doc.start_time && frm.doc.total_hours)
    {
        let total_min=frm.doc.total_hours*60
        let end_time=moment(frm.doc.start_time).add(total_min,"minutes").format("YYYY-MM-DD HH:mm:ss")
        frm.set_value("end_time",end_time);
        format_datetime_fields(frm);
    }
}
function format_datetime_fields(frm) {

    if (frm.doc.start_time) {
        let pretty_start = moment(frm.doc.start_time)
                            .format("DD MMM YYYY hh:mm A");

        // ✅ Directly set the input display value
        frm.fields_dict["start_time"]
            .$input
            .val(pretty_start);
    }

    if (frm.doc.end_time) {
        let pretty_end = moment(frm.doc.end_time)
                          .format("DD MMM YYYY hh:mm A");

        // ✅ Directly set the input display value
        frm.fields_dict["end_time"]
            .$input
            .val(pretty_end);
    }
}