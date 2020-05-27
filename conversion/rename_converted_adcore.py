import os
import re
import sys

adcore_release_tag = sys.argv[1]

# R3-2 -> V32
class_suffix = adcore_release_tag.replace('_', '').replace('-', '')
class_suffix = 'V' + class_suffix[1:]

source_extension = '.ui'
output_extension = f'_{class_suffix}.ui'  # .detailed.ui?

filename_map = {
    "ADAttrFile": "ADAttrFile",
    "ADBase": "_ADBase",  # do not match with ADBase class
    "ADBuffers": "ADBuffers",
    "ADCollect": "ADCollect",
    "ADDriverFile": "ADDriverFile",
    "ADEpicsShutter": "ADEpicsShutter",
    "ADPlugins": "ADPlugins",
    "ADReadout": "ADReadout",
    "ADSetup": "ADSetup",
    "ADShutter": "ADShutter",
    "ADTop": "ADTop",
    "NDCircularBuff": "CircularBuffPlugin",
    "NDCircularBuffHelp": "CircularBuffPluginHelp",
    "NDCodec": "CodecPlugin",
    "NDColorConvert": "ColorConvertPlugin",
    "NDFFT": "FFTPlugin",
    "NDFFT16": "FFT16",
    "NDFFTFreqSpectrumPlot": "FFTFreqSpectrumPlot",
    "NDFFTPlotAll": "FFTPlotAll",
    "NDFFTTimeSeriesPlot": "FFTTimeSeriesPlot",
    "NDFile": "FilePlugin",
    "NDFileBase": "FileBase",
    "NDFileHDF5": "HDF5Plugin",
    "NDFileHDF5_ChunkingFull": "HDF5Plugin_ChunkingFull",
    "NDFileHDF5_ExtraDims": "HDF5Plugin_ExtraDims",
    "NDFileHDF5_Positions": "HDF5Plugin_Positions",
    "NDFileJPEG": "JPEGPlugin",
    "NDFileMagick": "MagickPlugin",
    "NDFileNetCDF": "NetCDFPlugin",
    "NDFileNexus": "NexusPlugin",
    "NDFileNull": "NullPlugin",
    "NDFileTIFF": "TIFFPlugin",
    "NDGather8": "Gather8",
    "NDOverlay": "OverlayPlugin",
    "NDOverlay8": "Overlay8",
    "NDOverlayN": "OverlayN",
    "NDPlot": "Plot",
    "NDPlotXY": "PlotXY",
    "NDPluginAttribute": "AttributePlugin",
    "NDPluginAttribute8": "AttributePlugin8",
    "NDPluginBase": "PluginBase",
    "NDPluginBaseFull": "PluginBaseFull",
    "NDPluginTimeSeries": "TimeSeriesPlugin",
    "NDPluginTimeSeriesN": "TimeSeriesPluginN",
    "NDPos": "PosPlugin",   # <-- PosPluginPlugin typo in ophyd
    "NDProcess": "ProcessPlugin",
    "NDProcessTIFF": "ProcessTIFF",
    "NDPva": "PvaPlugin",
    "NDROI": "ROIPlugin",
    "NDROI4": "ROI4",
    "NDROIStat": "ROIStatPlugin",
    "NDROIStat8": "ROIStat8",
    "NDROIStatN": "ROIStatN",
    "NDScatter": "ScatterPlugin",
    "NDStats": "StatsPlugin",
    "NDStats5": "Stats5",
    "NDStatsTimeSeriesBasicAll": "StatsTimeSeriesBasicAll",
    "NDStatsTimeSeriesCentroidAll": "StatsTimeSeriesCentroidAll",
    "NDStatsTimeSeriesPlot": "StatsTimeSeriesPlot",
    "NDStdArrays": "ImagePlugin",  # <--
    "NDTimeSeries": "TimeSeries",
    "NDTimeSeriesPlot": "TimeSeriesPlot",
    "NDTransform": "TransformPlugin",
    "commonPlugins": "CommonPlugins",
    "createDirectoryHelp": "createDirectoryHelp",

    #
    "NDTimeSeriesAll": "TimeSeriesAll",
    "simDetector": "SimDetector",
    "simDetectorSetup": "SimDetectorSetup",
    "ADPvaDriver": "ADPvaDriver",
}


# Tag on the extensions
filename_map = {
    source + source_extension: dest + output_extension
    for source, dest in filename_map.items()
}

replace_regex = {
    re.compile(r'\b' + source + r'\b'): dest
    for source, dest in filename_map.items()
}

additional = list(display for display in
                  sorted(set(os.listdir()) - set(filename_map))
                  if os.path.splitext(display)[1] == '.ui')

for source, dest in filename_map.items():
    print('*', source, '->', dest)
    if not os.path.exists(source):
        continue

    with open(source, 'rt') as f:
        contents = f.read()

    for regex, sub in replace_regex.items():
        contents, count = regex.subn(sub, contents)
        if count > 0:
            print(f' - replaced {regex} -> {sub} {count} times')

    with open(dest, 'wt') as f:
        print(contents, file=f)


if additional:
    for screen in additional:
        print('!! Removing screen that was not renamed:', screen)
        os.unlink(screen)
