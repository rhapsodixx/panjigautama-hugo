---
title: "Video & Audio Codec Primer"
date: 2022-09-22T07:01:37
lastmod: 2022-09-22T07:04:08
slug: "video-audio-codec-primer"
draft: false
categories:
  - "Code"
  - "Streaming"
---

![](/images/original.gif)

This post is not intended to explain the video in a comprehensive manner but rather to distill important pieces of knowledge that are relevant to TipTip needs.

## Compression

Compression is a lossy process to shrink the size of the media, video in this case, to ensure the video can be streamed appropriately according to the user device's requirements. This process removes information; in a simple example, If two frames are basically identical, we can get rid of the data for one frame and replace it with a reference to the previous frame. Video compression has a lot of techniques; encoding is one of them.

wait, we can do lossless right? yes - but the file high likely is still too large for TipTip use case (and might not make sense anyway).

## Bitrate

Bit rate is the amount of data being processed within a given period of time – typically based on the number of bits per second that can be transmitted along a digital network. Higher bitrates mean a higher size of storage and potentially higher quality media.

## Encoding

Encoding is a process for altering the size of a video file, typically to make it smaller through **compression** without compromising on the quality.

if there is encoding, is there **decoding**? Yes, in the context of video streaming, a video player serves as a video decoder. The decoder's performance largely contributed to the latency of the video stream.

### Video Codec

Codec stands for enCOder and DECoder. As the name implies, the Encoder compresses the file and Decoded to decode the file on the player. Video may consist of Audio, each Video & Audio has a variety of Codec, and it comes with a variety of supported devices. Note that typically H264 is used up to 1080p resolution and H265/VP9/AV1 is up to 4K.

![](https://panjigautama.com/wp-content/uploads/2022/09/6f603544-2f95-4c57-9c5f-d26e71fd6c2b-1024x381.png)Bitmovin Definitive Guide of Video Codec

There’s a zero-cost entry level if one has less than 100K subscribers.

However, it's worth mentioning on utilizing **Multi-Codec** with AV1/VP9 in the near future (perhaps in early 2023) since [Apple is also rumored to support AV1](<https://www.neowin.net/news/apple-may-finally-be-adding-av1-codec-support-to-multiple-products/>) since [they have already joined the alliance](<https://www.winxdvd.com/video-transcoder/apple-device-av1-play.htm#:~:text=Apple%20joined%20the%20Alliance%20for,%2Dsource%20standard%20%2D%20AV1%20codec.>), royalty-free, and it has better compression rate.

### Audio Codec

  * Our best bet for audio codec is AAC
  * Opus is an option, but need further research on the compatibility and



Similar to video, audio also comes with various codecs with its own variety of device support. We excluded lossless codec since we are not audio heavy streaming platform at the moment, but we may consider doing so if we get into the music category.

| **AAC**| **MP3**| **Opus**  
---|---|---|---  
Compression| same audio quality as MP3 at a lower bitrate, and has more broader range of sampling rates/bit rates/and number of channels.| used to be industry leader but slowly replaced by other codec| Opus shows slightly superior quality compared to AAC and significantly better quality compared to Vorbis and MP3  
Browser Support| widely supported| well supported| supported by modern browser*  
Mobile Platform| widely supported| well suported| well suported  
Royalty| Non-free  
 _* no royalty fee for distribution_|  Non-free| Free  
  
#### Recommendation on the Bitrate

  * For a low-quality live stream (360p) video, use 64 Kbps audio bitrate
  * For a standard quality live stream like  480p and 720p video, use 128 Kbps audio bitrate
  * Audio bitrate for 1080p live video would be 256 Kbps 



Opus is considered the next king of the audio codec, with higher audio quality at all bitrates. Unlike Vorbis, [which is used by Spotify](<https://www.quora.com/Why-does-Spotify-use-the-relatively-obscure-Ogg-Vorbis-file-format>), Opus has support on both [iOS and Android](<https://www.xda-developers.com/ios-11-android-support-opus-audio-codec-mp3-successor/>) and modern browsers.

#### Recommendation on Channel

Generally speaking any video at 480p and above should use Stereo by default; we may consider mono for resolution below 480. How about the sample rate? I’d say we stick with the 16bit/44.1 kHz as that one is the standard. We have no absolute reason, at the moment, to go towards high-resolution audio files unless we somehow want to compete with Tidal, Apple Music, or similar business that focus on audio.

### Encoding & Bitrate

During an encode, video and audio components are split (a reference is kept for the decode) in 1-second segments; the segment length can be arbitrary, but the maximum is 10 seconds. Each the segments can be saved in a different quality/frame size by the encoder.

However, not all video files are equal; sports for instance is significantly larger in size and complexity than average ANIME.

![](/images/2c5f003c-cabb-4222-b516-6b936bbef05e.png)

### Transcoding

A more complex variation of encoding is transcoding, the process of converting one codec to another (or the same) codec – the process of compressing an already compressed file. Both decoding & encoding are necessary steps to achieving a successful transcode.

### Container

Container a.k.a Media Container a.k.a Container Formats is a metafile format describing multimedia data elements and metadata that coexist in files.

A container format provides the following:

  * **Stream Encapsulation**  
One or more media streams can exist in one single file.
  * **Timing/Synchronization**  
The container adds data on how the different streams in the file can be used together. E.g. The correct timestamps for synchronizing lip-movement in a video stream with speech found in the audio stream.
  * **Seeking**  
The container provides information to which point in time a movie can be jumped to. E.g. The viewer wants to watch only a part of a whole movie.
  * **Metadata**  
There are many flavours of metadata. It is possible to add them to a movie using a container format. E.g. the language of an audio stream.Sometimes subtitles are also considered as metadata.



![](/images/image6-1024x785-1.png)

As expected, the different container has different device of support, and it also requires a player to extract metadata from the container.

**MPEG-4 Part 14 (MP4)** is one of the most commonly used container formats and often has a .mp4 file ending. It is used for Dynamic Adaptive Streaming over HTTP (DASH) and can also be used for Apple’s HLS streaming. 

## Adaptive Bitrate Streaming

Note that the thing we discuss above is pretty much on one single video file being streamed over the internet a.k.a Progressive streaming – one resolution being used to multiple devices and screen resolutions.

![](/images/what-is-progressive-streaming.png)

It comes with two big major issues:

  * **Quality**  
720p video can’t play nicely on a 1080p screen, it will be stretched, and we can see pixelation.
  * **Buffering**  
If the user has a low-speed internet connection, the video needs to pause – wait for more data to be downloaded – and start again. This commonly happens on mobile devices.



Adaptive streaming enables video providers to create different videos for each audience (screen size/devices/internet speed). 

![](/images/what-is-adaptive-streaming-quality.png) ![](/images/what-is-adaptive-streaming-without-buffering.png)

We require to build manifest files (i.e. .m3u8 for HLS, .mpd for DASH).

![](/images/4f8a54f1-6633-4885-932d-4e0e9fa19074.png)

Note that the player on the client needs to support the ABR format since HLS & DASH have different support, though HLS has wider device and browser support. Note that DASH is codec agnostic, while HLS only supports H264/H265.

Typically what we need to do to support ABR:

  1. Produce video only & audio-only file
  2. Produce file segments (e.g. .ts)
  3. Produce .m3u8 playlist for each file segment
  4. Create a master .m3u8 file for the presentation



The above workflow is possible can be done with the well-known cloud/open source encoder like : [Bitmovin](<https://bitmovin.com/docs/encoding/tutorials/how-to-create-manifests-for-your-encodings>), Mux, FFMPEG, and bento4.

### ABR Format for Web Application

![](https://panjigautama.com/wp-content/uploads/2022/09/6b3e7ba4-803d-4385-bdce-a838746efcef-1024x871.png)<https://caniuse.com/?search=hls> as of 2022-09-15

### ABR Format for Mobile Application

At this time, Apple iOS devices must use HLS for content greater than 10 mins over a mobile network.

> <https://developer.apple.com/app-store/review/guidelines/>
> 
> **2.5.7** Video streaming content over a cellular network longer than 10 minutes must use HTTP Live Streaming and include a baseline 192 kbps HTTP Live stream.

For this reason, streams served to Apple devices are usually HLS, while DASH is used for other devices. However, Android supports HLS; please have a look at the Android documentation about [_Supported Media Formats_](<https://developer.android.com/guide/topics/media/media-formats.html#network>); there is also the ExoPlayer Open Source project, which supports MPEG-DASH& HLS. If we can only choose one for the time being, then we stick with HLS for mobile app.

## References

  * <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Video_codecs>
  * <https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Audio_codecs>
  * <https://github.com/cmpute/audio-codec-benchmark>
  * <https://bitmovin.com/audio-encoding/>
  * <https://bitmovin.com/encoding-definition-bitrates/>
  * <https://bitmovin.com/adaptive-streaming/>
  * <https://www.dacast.com/blog/best-audio-codec/>
  * <https://streaming4thepoor.live/as-a-small-business-must-i-pay-royalties-for-h264-and-h265/>
  * <https://amplify.nabshow.com/articles/bitrate-spend-a-compressed-guide-to-the-cost-of-codecs/>
  * <https://bitmovin.com/vp9-codec-status-quo/>
  * <https://streaminglearningcenter.com/learning/the-evolving-encoding-ladder-what-you-need-to-know.html#Table_2_Netflixs_per-title_can_change_both_the_number_of_rungs_and_their_resolution>
  * <https://netflixtechblog.com/per-title-encode-optimization-7e99442b62a2>
  * <https://bitmovin.com/top-video-technology-trends/>
  * <https://ottverse.com/mp3-aac-ac3-wav-wma-opus-audio-codecs-differences/>



[Bitmovin_UltimateGuidetoContainerFormats_Whitepaper](</images/Bitmovin_UltimateGuidetoContainerFormats_Whitepaper.pdf>)[Download](</images/Bitmovin_UltimateGuidetoContainerFormats_Whitepaper.pdf>)

[per-title-encoding-revised-1](</images/per-title-encoding-revised-1.pdf>)[Download](</images/per-title-encoding-revised-1.pdf>)
