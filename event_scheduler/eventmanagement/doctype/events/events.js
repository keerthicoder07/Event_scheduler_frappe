frappe.ui.form.on('Events', {

    refresh(frm) {
        // ✅ Only auto cancel needs realtime
        frappe.realtime.on("event_auto_cancelled", function(data) {
            frappe.show_alert({
                message:   data.message,
                indicator: "orange"
            }, 7);
            frm.reload_doc();
        });
    },

    onload_post_render(frm) {
        format_datetime_fields(frm);
    },

    start_time(frm) {
        calculate_end_time(frm);
        format_datetime_fields(frm);
    },

    total_hours(frm) {
        calculate_end_time(frm);
    },

    end_time(frm) {
        format_datetime_fields(frm);
    },

});


function calculate_end_time(frm) {
    if (frm.doc.start_time && frm.doc.total_hours) {
        let duration_minutes = frm.doc.total_hours * 60;
        let end_time = moment(frm.doc.start_time)
                        .add(duration_minutes, "minutes")
                        .format("YYYY-MM-DD HH:mm:ss");
        frm.set_value("end_time", end_time);
        format_datetime_fields(frm);
    }
}


function format_datetime_fields(frm) {
    if (frm.doc.start_time
        && frm.fields_dict.start_time
        && frm.fields_dict.start_time.$input) {
        frm.fields_dict["start_time"]
            .$input
            .val(moment(frm.doc.start_time)
            .format("DD MMM YYYY hh:mm A"));
    }

    if (frm.doc.end_time
        && frm.fields_dict.end_time
        && frm.fields_dict.end_time.$input) {
        frm.fields_dict["end_time"]
            .$input
            .val(moment(frm.doc.end_time)
            .format("DD MMM YYYY hh:mm A"));
    }
}