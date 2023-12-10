patches = {
    "Fallback Patch 1": [
        """case PipelineManager.FallbackStatus.Valid:
                        CurrentFallbackStatus = FallbackStatus.Compatible;
                        break;
                    default:
                        CurrentFallbackStatus = FallbackStatus.Incompatible;
                        break;""",
        """case PipelineManager.FallbackStatus.Valid:
                        CurrentFallbackStatus = FallbackStatus.Selectable;
                        break;
                    default:
                        CurrentFallbackStatus = FallbackStatus.Selectable;
                        break;"""
    ],
    "Fallback Patch 2": [
        """switch (pm.fallbackStatus)
                    {
                        case PipelineManager.FallbackStatus.Valid:
                            if (platforms.Contains("Windows") && platforms.Contains("Android") && Tools.Platform == "android")
                            {
                                CurrentFallbackStatus = FallbackStatus.Selectable;
                            }
                            else
                            {
                                CurrentFallbackStatus = FallbackStatus.Compatible;
                            }
                            break;
                        default:
                            CurrentFallbackStatus = FallbackStatus.Incompatible;
                            break;
                    }""",
        """if (platforms.Contains("Windows") && platforms.Contains("Android") && Tools.Platform == "android")
                    {
                        CurrentFallbackStatus = FallbackStatus.Selectable;
                    }
                    else
                    {
                        CurrentFallbackStatus = FallbackStatus.Compatible;
                    }"""
    ],
    "Upload Limits Patch 1": [
        """EditorUserBuildSettings.activeBuildTarget == BuildTarget.StandaloneWindows64) &&
                                         ((_builder.NoGuiErrorsOrIssuesForItem(_selectedAvatar) && _builder.NoGuiErrorsOrIssuesForItem(_builder)) || APIUser.CurrentUser.developerType ==
                                             APIUser.DeveloperType.Internal);""",
        "EditorUserBuildSettings.activeBuildTarget == BuildTarget.StandaloneWindows64);"
    ],
    "Upload Limits Patch 2": [
        """var uploadsAllowed = (_builder.NoGuiErrorsOrIssuesForItem(_selectedAvatar) && _builder.NoGuiErrorsOrIssuesForItem(_builder)) ||
                           APIUser.CurrentUser.developerType == APIUser.DeveloperType.Internal;""",
        "var uploadsAllowed = true;"
    ],
    "Upload Limits Patch 3": [
        """if (!_builder.NoGuiErrorsOrIssuesForItem(targetDescriptor) || !_builder.NoGuiErrorsOrIssuesForItem(_builder))
            {
                var errorsList = new List<string>();
                errorsList.AddRange(_builder.GetGuiErrorsOrIssuesForItem(targetDescriptor).Select(i => i.issueText));
                errorsList.AddRange(_builder.GetGuiErrorsOrIssuesForItem(_builder).Select(i => i.issueText));
                throw await HandleBuildError(new ValidationException("Avatar validation failed", errorsList));
            }""", ""
    ]
}

import os
import json
from tkinter import filedialog


class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKCYAN = '\033[96m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


class messages:
	SELECT_FOLDER_UNFORMATTED = "Select project folder to patch"
	SELECT_FOLDER = bcolors.WARNING + SELECT_FOLDER_UNFORMATTED + bcolors.ENDC
	NO_FOLDER_SELECTED = bcolors.FAIL + "No folder got selected" + bcolors.ENDC
	NO_PROJECT_SELECTED = bcolors.FAIL + "No project folder got selected" + bcolors.ENDC
	STARTING = bcolors.HEADER + "Starting to patch file" + bcolors.ENDC
	SAVED = bcolors.FAIL + "Saved patched file" + bcolors.ENDC


try:
	with open(
	    os.getenv('LOCALAPPDATA') + "\VRChatCreatorCompanion\settings.json",
	    "r") as f:
		defaultProjectPath = json.load(f)["defaultProjectPath"]
except (json.decoder.JSONDecodeError, FileNotFoundError):
	defaultProjectPath = None

print(messages.SELECT_FOLDER)

if defaultProjectPath:
	project_path = filedialog.askdirectory(
	    initialdir=defaultProjectPath,
	    title=messages.SELECT_FOLDER_UNFORMATTED)
else:
	project_path = filedialog.askdirectory(
	    title=messages.SELECT_FOLDER_UNFORMATTED)

if project_path == "":
	print(messages.NO_FOLDER_SELECTED)

file_path = project_path + "\Packages\com.vrchat.avatars\Editor\VRCSDK\SDK3A\VRCSdkControlPanelAvatarBuilder.cs"

print(messages.STARTING)

try:
	with open(file_path, "r") as f:
		file = f.read()
except FileNotFoundError:
	print(messages.NO_PROJECT_SELECTED)
	os.system('pause')
	exit(1)

for patch in patches:
	file = file.replace(patches[patch][0], patches[patch][1], 1)
	if patches[patch][1] != "":
		if patches[patch][1] in file:
			print(bcolors.OKGREEN + patch + " successfully" + bcolors.ENDC)
			continue
	elif patches[patch][0] not in file:
		print(bcolors.OKGREEN + patch + " successfully" + bcolors.ENDC)
		continue
	print(bcolors.FAIL + patch + " failed" + bcolors.ENDC)

with open(file_path, "w") as f:
	f.write(file)

print(messages.SAVED)
os.system('pause')
exit(0)
