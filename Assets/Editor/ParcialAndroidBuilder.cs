using System;
using System.IO;
using UnityEditor;
using UnityEditor.Build.Reporting;

public static class ParcialAndroidBuilder
{
    const string ScenePath = "Assets/Scenes/Parcial.unity";
    const string OutputPath = "Build/Parcial_RA.apk";

    [MenuItem("Build/Parcial Android APK")]
    public static void BuildAndroidApk()
    {
        Directory.CreateDirectory("Build");

        var options = new BuildPlayerOptions
        {
            scenes = new[] { ScenePath },
            locationPathName = OutputPath,
            target = BuildTarget.Android,
            options = BuildOptions.None
        };

        var report = BuildPipeline.BuildPlayer(options);
        var summary = report.summary;

        if (summary.result != BuildResult.Succeeded)
            throw new InvalidOperationException($"Android build failed: {summary.result}. See the Unity log for details.");

        UnityEngine.Debug.Log($"APK generado: {Path.GetFullPath(OutputPath)}");
    }
}
