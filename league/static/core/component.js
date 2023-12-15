const Component = {
    // token
    CsrfToken: $("#csrfToken"),
    // league module
    LeagueTable: $(".league-table"),
    ModalLeague: $("#leagueModal"),
    ModalButtonLeague: $("#modalLeague"),
    SaveButtonLeague: $("#saveLeague"),
    ModalLeagueField: {
        id: $("#leagueId"),
        homeName: $("#homeName"),
        homeScore: $("#homeScore"),
        awayName: $("#awayName"),
        awayScore: $("#awayScore"),
    },

    // team module
    TeamTable: $(".team-table"),
    ModalButtonTeam: $("#modalTeam"),
    ModalTeam: $("#teamsModal"),
    SaveButtonTeam: $("#saveTeams"),
    ModalTeamField: {
        id: $("#teamId"),
        name: $("#teamName"),
    },

    // statistic module
    StatisticTable: $(".statistic-table"),

    // upload module
    ModalButtonUpload: $("#modalUpload"),
    ModalUpload: $("#UploadModal"),
    DownloadButtonTemplate: $("#downloadTemplateUrl"),
    SaveButtonUpload: $("#saveFile"),
    ModalUploadField: {
        upload: $("#uploadFile"),
    },

    // rank module
    RankTable: $(".rank-table"),
};
