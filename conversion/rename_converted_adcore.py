import os
import re
import sys

SOURCE_EXTENSION = '.ui'
FILENAME_MAP = {
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
    "simDetector": "SimDetectorCam",
    "simDetectorSetup": "SimDetectorSetup",
    "ADPvaDriver": "ADPvaDriver",
}


def get_filename_map(output_extension):
    return {
        source + SOURCE_EXTENSION: dest + output_extension
        for source, dest in FILENAME_MAP.items()
    }


def get_class_suffix(adcore_release_tag):
    """R3-2 -> V32"""
    class_suffix = adcore_release_tag.replace('_', '').replace('-', '')
    return 'V' + class_suffix[1:]


def fix_ui_source(source, dest, replace_regex):
    """Fix the .ui source, as related display names have been renamed."""
    with open(source, 'rt') as f:
        contents = f.read()

    for regex, sub in replace_regex.items():
        contents, count = regex.subn(sub, contents)
        if count > 0:
            print(f' - replaced {regex} -> {sub} {count} times')

    with open(dest, 'wt') as f:
        print(contents, file=f)


def convert(adcore_release_tag, dest_path, *, class_suffix=None,
            output_extension=None):
    """
    Given the release tag, rename screens to typhos-compatible ones.

    Parameters
    ----------
    adcore_release_tag : str
        The release tag.

    dest_path : str
        The destination directory for the screens.

    class_suffix : str, optional
        Automatically determined by the release tag. e.g., ``R3-2`` is turned
        into a class suffix of ``_V32``.

    output_extension : str, optional
        Automatically determined by the release tag or class suffix. Defaults
        to f'_{class_suffix}.ui'.
    """

    if class_suffix is None:
        class_suffix = get_class_suffix(adcore_release_tag)

    if output_extension is None:
        output_extension = f'_{class_suffix}.ui'  # .detailed.ui?

    filename_map = get_filename_map(output_extension)
    replace_regex = {
        re.compile(r'\b' + source + r'\b'): dest
        for source, dest in filename_map.items()
    }

    replace_regex[re.compile(r'\${P}\${R}')] = '${prefix}'

    handled_filenames = set(list(filename_map) + list(filename_map.values()))
    other_displays = list(
        display for display in os.listdir()
        if os.path.splitext(display)[1] == '.ui' and
        display not in handled_filenames
    )

    for source, dest in filename_map.items():
        if os.path.exists(source):
            print('*', source, '->', dest)
            fix_ui_source(source, os.path.join(dest_path, dest), replace_regex)

    for display in other_displays:
        print('!! Unhandled display file:', display)


if __name__ == '__main__':
    adcore_release_tag = sys.argv[1]
    assert adcore_release_tag.startswith('R'), 'Bad release tag?'

    dest_path = sys.argv[2]
    assert os.path.exists(dest_path) and os.path.isdir(dest_path), 'Dest path?'

    if adcore_release_tag == 'R2-0':
        print('* Special-casing R2-0 to generate versionless screens.')
        convert(adcore_release_tag, dest_path, class_suffix='',
                output_extension='.ui')

    convert(adcore_release_tag, dest_path)
