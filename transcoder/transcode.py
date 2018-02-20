import boto3

client = boto3.client('elastictranscoder')


# response = client.create_job(
#     PipelineId='xxxxx-4mi8vh',
#     Inputs=[
#         {
#             'Key': 'media/220/spitch/165/1494515631633.mp4',
#             'FrameRate': 'auto',
#             'Resolution': 'auto',
#             'AspectRatio': 'auto',
#             'Interlaced': 'auto',
#             'Container': 'auto'
#         },
#         {
#             'Key': 'media/220/spitch/165/1494515641991.mp4',
#             'FrameRate': 'auto',
#             'Resolution': 'auto',
#             'AspectRatio': 'auto',
#             'Interlaced': 'auto',
#             'Container': 'auto'
#         },
#         {
#             'Key': 'media/220/spitch/165/1494515658681.mp4',
#             'FrameRate': 'auto',
#             'Resolution': 'auto',
#             'AspectRatio': 'auto',
#             'Interlaced': 'auto',
#             'Container': 'auto'
#         },
#         {
#             'Key': 'media/220/spitch/165/1494515666537.mp4',
#             'FrameRate': 'auto',
#             'Resolution': 'auto',
#             'AspectRatio': 'auto',
#             'Interlaced': 'auto',
#             'Container': 'auto'
#         },
#     ],
#     Output={
#         'Key': 'transcoder.mp4',
#         'ThumbnailPattern': 'thumbnnail-{count}',
#         'Rotate': 'auto',
#         'PresetId': 'xxxxxx-iavt4y',
#         'Watermarks': [
#             {
#                 'PresetWatermarkId': 'BottomRight',
#                 'InputKey': 'media/default/logo-blanc.png'
#             },
#         ]
#     },
#     OutputKeyPrefix='media/220/spitch/165/trans/'
# ) 



response = client.create_job(
    PipelineId='xxxxxxx-truz2h',
    Input=
        {
            'Key': 'media/235/spitch/942/118b962300904dbab7b6.mp4',
            'FrameRate': 'auto',
            'Resolution': 'auto',
            'AspectRatio': 'auto',
            'Interlaced': 'auto',
            'Container': 'auto'
        },
    Output={
        'Key': 'transcoder-07.mp4',
        'Rotate': 'auto',
        'PresetId': 'xxxxxxx-3cssbu'
    },
    OutputKeyPrefix='media/235/spitch/942/'
)

print(response)
