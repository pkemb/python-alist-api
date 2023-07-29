alist.admin
===========

.. autoclass:: alist.admin.AlistAdmin
   :members:
   :undoc-members:
   :show-inheritance:



admin setting
-------------

.. class:: alist.admin.AlistAdmin
   :noindex:

   .. method:: setting_version()

      获取version

      .. code-block:: python

         version = client.admin.setting_version()

   .. method:: setting_title(new = None)

      获取或更新title。

      :param new: 如果不为None，则更新title

      .. code-block:: python

         # 更新标题为'new title'
         client.admin.setting_title('new title')

      类似的API还有：

      - setting_logo(new = None)
      - setting_favicon(new = None)
      - setting_icon_color(new = None)
      - setting_announcement(new = None)
      - setting_text_types(new = None)
      - setting_audio_types(new = None)
      - setting_video_types(new = None)
      - setting_hide_files(new = None)
      - setting_music_cover(new = None)
      - setting_site_beian(new = None)
      - setting_global_readme_url(new = None)
      - setting_pdf_viewer_url(new = None)
      - setting_autoplay_video(new = None)
      - setting_autoplay_audio(new = None)
      - setting_customize_head(new = None)
      - setting_customize_body(new = None)
      - setting_home_emoji(new = None)
      - setting_animation(new = None)
      - setting_artplayer_whitelist(new = None)
      - setting_artplayer_autoSize(new = None)
      - setting_load_type(new = None)
      - setting_default_page_size(new = None)
      - setting_password(new = None)
      - setting_d_proxy_types(new = None)
      - setting_check_parent_folder(new = None)
      - setting_check_down_link(new = None)
      - setting_WebDAV_username(new = None)
      - setting_WebDAV_password(new = None)
      - setting_Visitor_WebDAV_username(new = None)
      - setting_Visitor_WebDAV_password(new = None)
      - setting_ocr_api(new = None)
      - setting_enable_search(new = None)
      - setting_Aria2_RPC_url(new = None)
      - setting_Aria2_RPC_secret(new = None)

