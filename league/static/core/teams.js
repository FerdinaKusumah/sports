// on click create new teams
Component.ModalButtonTeam.on("click", function () {
    Component.ModalTeam.modal("show");
});

// save new teams
Component.SaveButtonTeam.on("click", function () {
    if (Component.ModalTeamField.name.val().length === 0) return;

    // if no id then create
    if (Component.ModalTeamField.id.val().length === 0) {
        const url = Constants.TeamUrl;
        const payload = {"name": Component.ModalTeamField.name.val()};
        Rest.post(url, payload)
            .done(function () {
                TeamsTable.ajax.reload();
            })
            .fail(function () {
                TeamsTable.ajax.reload();
            })
            .always(function () {
                Component.ModalTeam.modal("hide");
            });

    } else {
        const url = `${Constants.TeamUrl}/${Component.ModalTeamField.id.val()}`;
        const payload = {"name": Component.ModalTeamField.name.val()};
        Rest.put(url, payload)
            .done(function () {
                TeamsTable.ajax.reload();
                LeagueTable.ajax.reload();
                StatisticTable.ajax.reload();
                rankTable.ajax.reload();
            })
            .fail(function () {
                TeamsTable.ajax.reload();
                LeagueTable.ajax.reload();
                StatisticTable.ajax.reload();
                rankTable.ajax.reload();
            })
            .always(function () {
                Component.ModalTeam.modal("hide");
            });
    }
    Component.ModalTeamField.name.val("");
});

// function edit teams
TeamsTable.on('click', 'tbody > tr > td > button', function () {
    const data = TeamsTable.row($(this).closest("td")).data();
    const attr = $(this).attr("data-model-name");
    if (attr === "edit") {
        Component.ModalTeamField.name.val(data.name);
        Component.ModalTeam.modal("show");
        Component.ModalTeamField.id.val(data.id);
    } else {
        const url = `${Constants.TeamUrl}/${data.id}`;
        Rest.delete(url)
            .done(function () {
                TeamsTable.ajax.reload();
            })
            .fail(function () {
                TeamsTable.ajax.reload();
            })
            .always(function () {
                TeamsTable.ajax.reload();
            });
    }
});
