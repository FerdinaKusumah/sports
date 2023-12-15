// on click create new league
Component.ModalButtonLeague.on("click", function () {
    // fetch data teams
    const url = Constants.TeamUrl;
    Rest.get(url)
        .done(function (resp) {
            $.each(resp.data, function (key, val) {
                Component.ModalLeagueField.homeName.append(new Option(val.name, val.id));
                Component.ModalLeagueField.awayName.append(new Option(val.name, val.id));
            });
        })
        .fail(function (err) {
            console.log(err);
        })
        .always(function () {
            Component.ModalLeague.modal("show");
        });
});

// save new league
Component.SaveButtonLeague.on("click", function () {
    const homeNameEmpty = Component.ModalLeagueField.homeName.val().length === 0;
    const awayNameEmpty = Component.ModalLeagueField.awayName.val().length === 0;
    const homeScoreEmpty = Component.ModalLeagueField.homeScore.val().length === 0;
    const awayScoreEmpty = Component.ModalLeagueField.awayScore.val().length === 0;
    if (homeNameEmpty || awayNameEmpty || homeScoreEmpty || awayScoreEmpty) return;

    const payload = {
        "home_id": Component.ModalLeagueField.homeName.val(),
        "away_id": Component.ModalLeagueField.awayName.val(),
        "home_score": Component.ModalLeagueField.homeScore.val(),
        "away_score": Component.ModalLeagueField.awayScore.val(),
    };
    // if no id then create
    if (Component.ModalLeagueField.id.val().length === 0) {
        const url = Constants.LeagueUrl;
        Rest.post(url, payload)
            .done(function () {
                LeagueTable.ajax.reload();
                StatisticTable.ajax.reload();
                rankTable.ajax.reload();
            })
            .fail(function (err) {
                console.log(err);
            })
            .always(function () {
                Component.ModalLeague.modal("hide");
            });
    } else {
        const url = `${Constants.LeagueUrl}/${Component.ModalLeagueField.id.val()}`;
        Rest.put(url, payload)
            .done(function () {
                LeagueTable.ajax.reload();
                StatisticTable.ajax.reload();
                rankTable.ajax.reload();
            })
            .fail(function (err) {
                console.log(err);
            })
            .always(function () {
                Component.ModalLeague.modal("hide");
            });
    }

    Component.ModalLeagueField.homeName.children().remove();
    Component.ModalLeagueField.awayName.children().remove();
    Component.ModalLeagueField.homeScore.val("");
    Component.ModalLeagueField.awayScore.val("");
});

// function edit league
LeagueTable.on('click', 'tbody > tr > td > button', function () {
    const data = LeagueTable.row($(this).closest("td")).data();
    const attr = $(this).attr("data-model-name");
    if (attr === "edit") {
        // fetch data teams
        const url = Constants.TeamUrl;
        Rest.get(url)
            .done(function (resp) {
                $.each(resp.data, function (key, val) {
                    Component.ModalLeagueField.homeName.append(new Option(val.name, val.id));
                    Component.ModalLeagueField.awayName.append(new Option(val.name, val.id));
                });

                Component.ModalLeagueField.id.val(data.id);
                Component.ModalLeagueField.homeName.val(data.home_id);
                Component.ModalLeagueField.awayName.val(data.away_id);
                Component.ModalLeagueField.homeScore.val(data.home_score);
                Component.ModalLeagueField.awayScore.val(data.away_score);
            })
            .fail(function (err) {
                console.log(err);
            })
            .always(function () {
                Component.ModalLeague.modal("show");
            });
    } else {
        const url = `${Constants.LeagueUrl}/${data.id}`;
        Rest.delete(url)
            .done(function () {
                LeagueTable.ajax.reload();
            })
            .fail(function (err) {
                console.log(err);
            })
            .always(function () {
                LeagueTable.ajax.reload();
            });
    }
});
