using UnrealBuildTool;
public class TN_Bus_Realistic : ModuleRules
{
    public TN_Bus_Realistic(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore" });
    }
}
