CKEDITOR.on( 'instanceReady', function(ev){
    const editor = ev.editor;

    editor.on('fileUploadRequest', function(ev){
        const fileLoader = ev.data.fileLoader;
        //By binding Notifications, notifications will appear on the main edit screen, but this time it's a different Dialog, so it doesn't make much sense.
        // CKEDITOR.fileTools.bindNotifications(fileLoader.editor, fileLoader);

        fileLoader.on("uploading", function () {
            console.log("Start uploading");
        });

        fileLoader.on("uploaded", function () {
            console.log("Upload completed");
        });

        fileLoader.on("error", function () {
            console.log("Upload error");
        });

        fileLoader.on("abort", function () {
            console.log("Upload failure");
        });
    });
});