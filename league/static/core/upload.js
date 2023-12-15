// onclick bulk upload csv
Component.ModalButtonUpload.on("click", function () {
    Component.DownloadButtonTemplate.attr("href", Constants.UploadUrl);
    Component.ModalUpload.modal("show");
});
// save upload
Component.SaveButtonUpload.on("click", function () {
    const file = Component.ModalUploadField.upload.prop("files");
    if (file.length === 0) return;

    const fileToUpload = file[0];
    const formData = new FormData();
    formData.append("file", fileToUpload);

    Rest.upload(Constants.UploadUrl, formData)
        .done(function () {
            // refresh all table
            TeamsTable.ajax.reload();
            LeagueTable.ajax.reload();
            StatisticTable.ajax.reload();
            rankTable.ajax.reload();
        })
        .fail(function (err) {
            console.log(err);
        })
        .always(function () {
            // remove file input
            Component.ModalUploadField.upload.val("");
            Component.ModalUpload.modal("hide");
        });
});
