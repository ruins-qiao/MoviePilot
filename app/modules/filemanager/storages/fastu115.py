from pathlib import Path
from typing import TYPE_CHECKING, Optional

from app.log import logger
from app.schemas import FileItem as _FileItem

if TYPE_CHECKING:
    from app.modules.filemanager.storages.u115 import U115Pan


class U115PanFast:
    """115 仅秒传上传通道，不参与普通存储类型注册。"""

    def __init__(self, storage: "U115Pan"):
        """初始化快速上传通道。

        :param storage: 已初始化的 115 存储实例
        """
        self.storage = storage

    def upload(
        self,
        target_dir: _FileItem,
        local_path: Path,
        new_name: Optional[str] = None,
    ) -> Optional[_FileItem]:
        """尝试将本地文件秒传到 115，未命中时返回 None。

        :param target_dir: 115 目标目录
        :param local_path: 本地文件路径
        :param new_name: 上传后的文件名
        :return: 秒传成功后的文件项，未命中或请求失败时返回 None
        """
        try:
            return self.storage.upload(
                target_dir,
                local_path,
                new_name,
                fast_only=True,
            )
        except Exception as err:
            logger.warning(f"【115】仅秒传请求失败，跳过本轮：{str(err)}")
            return None
