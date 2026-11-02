Set objShell = CreateObject("WScript.Shell")
Set fileSystem = CreateObject("Scripting.FileSystemObject")
projectDir = fileSystem.GetParentFolderName(WScript.ScriptFullName)
objShell.CurrentDirectory = projectDir
objShell.Run """" & fileSystem.BuildPath(projectDir, "run.bat") & """", 0, False
