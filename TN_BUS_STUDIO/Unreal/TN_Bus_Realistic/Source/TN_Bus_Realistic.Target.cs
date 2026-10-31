using UnrealBuildTool;
using System.Collections.Generic;
public class TN_Bus_RealisticTarget : TargetRules
{
    public TN_Bus_RealisticTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.V5;
        ExtraModuleNames.Add("TN_Bus_Realistic");
    }
}
