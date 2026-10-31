using UnrealBuildTool;
using System.Collections.Generic;
public class TN_Bus_RealisticEditorTarget : TargetRules
{
    public TN_Bus_RealisticEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        ExtraModuleNames.Add("TN_Bus_Realistic");
    }
}
