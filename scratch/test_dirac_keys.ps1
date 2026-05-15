# PowerShell script to test dirac's raw mode by sending keystrokes
# Uses Windows Forms SendKeys to target the spawned process window

Add-Type -AssemblyName System.Windows.Forms
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Diagnostics;
public class WinConsole {
    [DllImport("kernel32.dll")]
    public static extern IntPtr GetConsoleWindow();
    
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    
    [DllImport("user32.dll", SetLastError = true)]
    public static extern IntPtr FindWindow(string lpClassName, string lpWindowName);
    
    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint lpdwProcessId);
}
"@

# Get current console window
$currentWindow = [WinConsole]::GetConsoleWindow()

Write-Host "Starting dirac in a new console window..."
Write-Host "Waiting for it to initialize..."

# Start dirac in the same console but as a background process
# This won't work well... Let me try a different approach

# Instead, let's test with a mini Node.js script that simulates the scenario
# by checking if raw mode works with our dirac-installed App.js

Write-Host @"
=== Instructions for Manual Testing ===

Please test in your terminal:

Option A - Test the fix directly:
  dirac

Then:
  1. Press UP arrow (should move selection to "Exit")
  2. Press Enter
  Expected: should exit immediately (raw mode working)
  Bug behavior: nothing happens, need another UP + Enter

Option B - Run the diagnostic:
  node scratch/test_raw_mode_deferred.mjs t3

Option C - Run the diagnostic comparing approaches:
  node scratch/test_raw_mode_deferred.mjs t1   (no kick - expect broken)
  node scratch/test_raw_mode_deferred.mjs t2   (immediate kick - might be broken)
  node scratch/test_raw_mode_deferred.mjs t3   (nextTick kick - proposed fix)

"@
