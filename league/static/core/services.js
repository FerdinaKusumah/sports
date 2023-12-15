const Rest = {
    get: function (url) {
        const deferred = $.Deferred();
        $.ajax({
            url: url,
            contentType: "application/json",
            headers: {"X-CSRFToken": Component.CsrfToken.val()},
            method: 'GET',
            success: function (data) {
                // Resolve the Deferred with the data
                deferred.resolve(data);
            },
            error: function (error) {
                // Reject the Deferred with the error
                deferred.reject(error);
            }
        });
        // Return the promise
        return deferred.promise();
    },
    post: function (url, data) {
        const deferred = $.Deferred();
        $.ajax({
            url: url,
            contentType: "application/json",
            headers: {"X-CSRFToken": Component.CsrfToken.val()},
            data: JSON.stringify(data),
            method: 'POST',
            success: function (data) {
                // Resolve the Deferred with the data
                deferred.resolve(data);
            },
            error: function (error) {
                // Reject the Deferred with the error
                deferred.reject(error);
            }
        });
        // Return the promise
        return deferred.promise();
    },
    put: function (url, data) {
        const deferred = $.Deferred();
        $.ajax({
            url: url,
            contentType: "application/json",
            headers: {"X-CSRFToken": Component.CsrfToken.val()},
            data: JSON.stringify(data),
            method: 'PUT',
            success: function (data) {
                // Resolve the Deferred with the data
                deferred.resolve(data);
            },
            error: function (error) {
                // Reject the Deferred with the error
                deferred.reject(error);
            }
        });
        // Return the promise
        return deferred.promise();
    },
    delete: function (url) {
        const deferred = $.Deferred();
        $.ajax({
            url: url,
            contentType: "application/json",
            headers: {"X-CSRFToken": Component.CsrfToken.val()},
            method: 'DELETE',
            success: function (data) {
                // Resolve the Deferred with the data
                deferred.resolve(data);
            },
            error: function (error) {
                // Reject the Deferred with the error
                deferred.reject(error);
            }
        });
        // Return the promise
        return deferred.promise();
    },
    upload: function (url, formData) {
        const deferred = $.Deferred();

        $.ajax({
            method: "POST",
            url: url,
            headers: {"X-CSRFToken": Component.CsrfToken.val()},
            data: formData,
            processData: false,
            contentType: false,
            success: function (data) {
                // Resolve the Deferred with the data
                deferred.resolve(data);
            },
            error: function (error) {
                // Reject the Deferred with the error
                deferred.reject(error);
            }
        });
        // Return the promise
        return deferred.promise();
    }
};
