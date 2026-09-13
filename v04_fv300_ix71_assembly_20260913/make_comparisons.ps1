Add-Type -AssemblyName System.Drawing
$fvOut=$PSScriptRoot
$fvRepo=Split-Path -Parent $fvOut
function Read-FVImage([string]$path){
 $im=[System.Drawing.Image]::FromFile($path)
 if($im.PropertyIdList -contains 274){
  $ori=[BitConverter]::ToUInt16($im.GetPropertyItem(274).Value,0)
  switch($ori){3{$im.RotateFlip([System.Drawing.RotateFlipType]::Rotate180FlipNone)}6{$im.RotateFlip([System.Drawing.RotateFlipType]::Rotate90FlipNone)}8{$im.RotateFlip([System.Drawing.RotateFlipType]::Rotate270FlipNone)}}
 }
 return $im
}
function New-FVPair([string]$left,[string]$right,[string]$dest,[string]$leftTitle,[string]$rightTitle,[int]$panelWidth=900,[int]$panelHeight=1400){
 $fvL=Read-FVImage $left
 $fvR=Read-FVImage $right
 $fvB=New-Object System.Drawing.Bitmap ($panelWidth*2),($panelHeight+70)
 $fvG=[System.Drawing.Graphics]::FromImage($fvB)
 $fvG.Clear([System.Drawing.Color]::White)
 $fvG.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
 $fvFont=New-Object System.Drawing.Font 'Arial',20
 $fvG.DrawString($leftTitle,$fvFont,[System.Drawing.Brushes]::Black,14,20)
 $fvG.DrawString($rightTitle,$fvFont,[System.Drawing.Brushes]::Black,($panelWidth+14),20)
 $fvIdx=0
 foreach($fvIm in @($fvL,$fvR)){
  $fvScale=[Math]::Min($panelWidth/$fvIm.Width,$panelHeight/$fvIm.Height)
  $fvW=[int]($fvIm.Width*$fvScale);$fvH=[int]($fvIm.Height*$fvScale)
  $fvX=[int]($fvIdx*$panelWidth+($panelWidth-$fvW)/2);$fvY=[int](70+($panelHeight-$fvH)/2)
  $fvG.DrawImage($fvIm,$fvX,$fvY,$fvW,$fvH)
  $fvIdx++
 }
 $fvB.Save($dest,[System.Drawing.Imaging.ImageFormat]::Jpeg)
 $fvG.Dispose();$fvB.Dispose();$fvFont.Dispose();$fvL.Dispose();$fvR.Dispose()
}
New-FVPair "$fvRepo\20260910_153139.jpg" "$fvOut\07_photo153139_front_detail.png" "$fvOut\compare_153139.jpg" 'YOUR PHOTO - 153139' 'ROUND 1 - approximate view'
New-FVPair "$fvRepo\20260910_153147.jpg" "$fvOut\08_photo153147_side_detail.png" "$fvOut\compare_153147.jpg" 'YOUR PHOTO - 153147' 'ROUND 1 - approximate view'
New-FVPair "$fvRepo\20260910_153221.jpg" "$fvOut\09_photo153221_illumination.png" "$fvOut\compare_153221.jpg" 'YOUR PHOTO - 153221' 'ROUND 1 - approximate view'
New-FVPair "$fvOut\references\fv300_ix71_catalog_configuration.png" "$fvOut\11_catalog_approx.png" "$fvOut\compare_catalog_assembly.jpg" 'OLYMPUS FV300 brochure p1' 'ROUND 1 - dimensions partly estimated' 1200 1000

