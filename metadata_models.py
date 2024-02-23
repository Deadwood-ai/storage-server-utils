from enum import Enum
from datetime import datetime

from pydantic import BaseModel, field_serializer, computed_field


class PlatformEnum(str, Enum):
    drone = "drone"
    airborne = "airborne"
    sattelite = "sattelite"


class LicenseEnum(str, Enum):
    cc_by = "cc-by"
    cc_by_sa = "cc-by-sa"


class StatusEnum(str, Enum):
    pending = "pending"
    processing = "processing"
    errored = "errored"
    processed = "processed"
    audited = "audited"
    audit_failed = "audit_failed"


class FileUploadMetadata(BaseModel):
    user_id: str
    aquisition_date: datetime
    upload_date: datetime
    file_name: str
    content_type: str
    file_size: int
    target_path: str
    copy_time: float
    uuid: str
    sha256: str
    platform: PlatformEnum
    license: LicenseEnum
    status: StatusEnum = StatusEnum.pending

    @computed_field
    @property
    def file_id(self) -> str:
        return f"{self.uuid}_{self.file_name}"
    
    @field_serializer('aquisition_date', 'upload_date', mode='plain')
    def datetime_to_isoformat(field: datetime) -> str:
        return field.isoformat()
