var shortcutName = "ExploraOS.lnk";
var scriptDir = WScript.ScriptFullName.replace(/[^\\]+$/, "");
var targetPath = scriptDir + "explora_player.pyw";
var iconPath = scriptDir + "exploraOSicon.ico";
var desktopPath = WScript.CreateObject("WScript.Shell").SpecialFolders("Desktop");


function createShortcut() {
    var shell = WScript.CreateObject("WScript.Shell");
    var shortcut = shell.CreateShortcut(desktopPath + "\\" + shortcutName);
    shortcut.TargetPath = "pythonw.exe";
    shortcut.Arguments = targetPath;
    shortcut.WorkingDirectory = scriptDir;
    shortcut.IconLocation = iconPath;
    shortcut.Save();
}


var fso = new ActiveXObject("Scripting.FileSystemObject");
if (fso.FileExists(iconPath)) {
    createShortcut();
    //WScript.Echo("Shortcut created at " + desktopPath + "\\" + shortcutName);
} else {
    WScript.Echo("Icon file not found: " + iconPath);
}

// MADE WITH HELP