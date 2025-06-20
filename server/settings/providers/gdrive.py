from pydantic import Field

from ayon_server.settings import BaseSettingsModel


class CredPathPerPlatform(BaseSettingsModel):
    windows: list[str] = Field(default_factory=list,
                               scope=["studio", "project", "site"],)
    linux: list[str] = Field(default_factory=list,
                             scope=["studio", "project", "site"],)
    darwin: list[str] = Field(default_factory=list,
                              scope=["studio", "project", "site"],)


def gdrive_account_resolver():
    """Return a list of value/label dicts for the enumerator.

    Returning a list of dicts is used to allow for a custom label to be
    displayed in the UI.
    """
    gdrive_acc_type_dict = {
        1: "business", 2:"personal"
    }
    return [{"value": f"{key}", "label": f"{label}"}
            for key, label in gdrive_acc_type_dict.items()]

gdrive_type_enum = gdrive_account_resolver()

class GoogleDriveSubmodel(BaseSettingsModel):
    """Specific settings for Google Drive sites.

    credentials_url: .json file for service account which must have access
        to shared GDrive folder/drive
    root: root folder on GDrive, `/My Drive` prefix is required for classic
        GDrive, shared disks don't need that
    """
    _layout = "expanded"
    credentials_url: CredPathPerPlatform = Field(
        title="Credentials url",
        scope=["studio", "project", "site"],
        default_factory=CredPathPerPlatform,
        description="""Path to credentials .json available on shared disk."""
    )

    roots: str = Field(
        "",
        title="GDrive root folder",
        scope=["studio", "project"],
        description="Root folder on Google Drive",
    )

    account_type: str = Field(
        "",
        title="Account Type",
        description="Switch between GDrive account types",
        enum_resolver=lambda: gdrive_type_enum,
        conditionalEnum=True
    )