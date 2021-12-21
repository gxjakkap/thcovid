from os.path    import join
from os         import remove

from discord    import HTTPException
from emoji      import emojize

import settings


# Returns a path relative to the bot directory
def get_rel_path(rel_path):
    return join(settings.BASE_DIR, rel_path)


# Returns an emoji as required to send it in a message
# You can pass the emoji name with or without colons
# If fail_silently is True, it will not raise an exception
# if the emoji is not found, it will return the input instead
def get_emoji(emoji_name, fail_silently=False):
    alias = emoji_name if emoji_name[0] == emoji_name[-1] == ":" \
            else f":{emoji_name}:"
    the_emoji = emojize(alias, use_aliases=True)

    if the_emoji == alias and not fail_silently:
        raise ValueError(f"Emoji {alias} not found!")

    return the_emoji


# A shortcut to get a channel by a certain attribute
# Uses the channel name by default
# If many matching channels are found, returns the first one
def get_channel(client, value, attribute="name"):
    channel = next((c for c in client.get_all_channels() 
                    if getattr(c, attribute).lower() == value.lower()), None)
    if not channel:
        raise ValueError("No such channel")
    return channel


# Shortcut method to send a message in a channel with a certain name
# You can pass more positional arguments to send_message
# Uses get_channel, so you should be sure that the bot has access to only
# one channel with such name
async def send_in_channel(client, channel_name, *args):
    await client.send_message(get_channel(client, channel_name), *args)


# Attempts to upload a file in a certain channel
# content refers to the additional text that can be sent alongside the file
# delete_after_send can be set to True to delete the file afterwards
async def try_upload_file(client, channel, file_path, content=None, 
                          delete_after_send=False, retries=3):
    used_retries = 0
    sent_msg = None

    while not sent_msg and used_retries < retries:
        try:
            sent_msg = await client.send_file(channel, file_path,
                                              content=content)
        except HTTPException:
            used_retries += 1

    if delete_after_send:
        remove(file_path)

    if not sent_msg:
        await client.send_message(channel,
                                 "Oops, something happened. Please try again.")

    return sent_msg



# Custom function to check if user input is a valid province name
def checkprovincevalidity(input):
    thai_pr = ["กรุงเทพมหานคร", "กระบี่", "กาญจนบุรี", "กาฬสินธุ์", "กำแพงเพชร", "ขอนแก่น", "จันทบุรี", "ฉะเชิงเทรา", "ชลบุรี", "ชัยนาท", "ชัยภูมิ", "ชุมพร ", "เชียงราย", "เชียงใหม่", "ตรัง", "ตราด", "ตาก", "นครนายก", "นครปฐม", "นครพนม", "นครราชสีมา", "นครศรีธรรมราช", "นครสวรรค์", "นนทบุรี", "นราธิวาส", "น่าน", "บึงกาฬ", "บุรีรัมย์", "ปทุมธานี", "ประจวบคีรีขันธ์", "ปราจีนบุรี", "ปัตตานี", "พระนครศรีอยุธยา", "พะเยา", "พังงา", "พัทลุง", "พิจิตร", "พิษณุโลก", "เพชรบุรี", "เพชรบูรณ์", "แพร่", "ภูเก็ต", "มหาสารคาม", "มุกดาหาร", "แม่ฮ่องสอน", "ยโสธร", "ยะลา", "ร้อยเอ็ด", "ระนอง", "ระยอง", "ราชบุรี", "ลพบุรี", "ลำปาง", "ลำพูน", "เลย", "ศรีสะเกษ", "สกลนคร", "สงขลา", "สตูล", "สมุทรปราการ", "สมุทรสงคราม", "สมุทรสาคร", "สระแก้ว", "สระบุรี", "สิงห์บุรี", "สุโขทัย", "สุพรรณบุรี", "สุราษฎร์ธานี", "สุรินทร์", "หนองคาย", "หนองบัวลำภู", "อ่างทอง", "อำนาจเจริญ", "อุดรธานี", "อุตรดิตถ์", "อุทัยธานี", "อุบลราชธานี"]
    eng_pr = ["BANGKOK","KRABI","KANCHANABURI","KALASIN","KAMPHAENG PHET","KHON KAEN","CHANTHABURI","CHACHOENGSAO","CHON BURI","CHAI NAT","CHAIYAPHUM","CHUMPHON","CHIANG RAI","CHIANG MAI","TRANG","TRAT","TAK","NAKHON NAYOK","NAKHON PATHOM","NAKHON PHANOM","NAKHON RATCHASIMA","NAKHON SI THAMMARAT","NAKHON SAWAN","NONTHABURI","NARATHIWAT","NAN","BUENG KAN","BURI RAM","PATHUM THANI","PRACHUAP KHIRI KHAN","PRACHIN BURI","PATTANI","PHRA NAKHON SI AYUTTHAYA","PHAYAO","PHANGNGA","PHATTHALUNG","PHICHIT","PHITSANULOK","PHETCHABURI","PHETCHABUN","PHRAE","PHUKET","MAHA SARAKHAM","MUKDAHAN","MAE HONG SON","YASOTHON","YALA","ROI ET","RANONG","RAYONG","RATCHABURI","LOP BURI","LAMPANG","LAMPHUN","LOEI","SI SA KET","SAKON NAKHON","SONGKHLA","SATUN","SAMUT PRAKAN","SAMUT SONGKHRAM","SAMUT SAKHON","SA KAEO","SARABURI","SING BURI","SUKHOTHAI","SUPHAN BURI","SURAT THANI","SURIN","NONG KHAI","NONG BUA LAM PHU","ANG THONG","AMNAT CHAROEN","UDON THANI","UTTARADIT","UTHAI THANI","UBON RATCHATHANI"]
    eng_abr = []

    if input in thai_pr:
        return [True, input]
    elif input.upper() in eng_pr:
        return [True, thai_pr[eng_pr.index(input.upper())]]
    elif input in eng_abr:
        return [True, thai_pr[eng_pr.index(input)]]
    else:
        return [False]