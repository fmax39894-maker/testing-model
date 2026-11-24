import os
import json
import random
import logging
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
TIMEOUT = 12
MAX_IMAGE_BYTES = 8 * 1024 * 1024

# Add your public image/page URLs here. Keep each URL in quotes.
IMAGE_LINKS = [
        "http://sigmapics.net/images/xxxsexpic.net/0/093_brunette_for.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/172/000_set_.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/561_selfies_selfies.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/843_swinger_photos.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/122/006_cute_amateur.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/471_cock_like.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/133/668_Hirsute_getting.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/693_milf_Charlee.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/13/995_set_public.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/116/168_doggy_satisfied.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/14/200_ample_ample.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/35/860_amateur_boned.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/35/875_with_babe.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/191/485_set_set.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/497_with_attention.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/132/888_porn_porn.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/3/143_Brooke_Clothed.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/130/524_her_soaking.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/230/856_and_hard.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/062_Petite_blonde.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/536_7_public.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/207/248_Geeky_girls.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/234/693_a_face.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/118/936_fucked_ass.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/189/118__set.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/511_xx_.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/931_in_jeans.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/228_dozen_of.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/3/113__and.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/227/404_fuck_Euro.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/334_trying_him.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/15/615_bath_teen.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/846_cel_set.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/216/487_xx_xx.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/882_her_her.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/567_pussy_brunette.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/911_88_public.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/006_true_face.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/810_cunt_so.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/36/168_harem_sex.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/170/266_red_off.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/3/218_casting_teen.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/424_cel_.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/583_getting_outdoors.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/130/539_set_233.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/468_Is_Back.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/416_her_natural.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/721__26.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/239/218_getting_chick.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/234/644_a_kink.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/227/888_xx_.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/220/062__set.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/134/082_blonde_blonde.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/12/475_sex_with.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/170/514_Innocent_carrot.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/116/485_their_pussies.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/36/138_sex_sex.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/36/227_nude_petite.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/174/455_amateur_Compilation.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/352_naked_poses.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/215/582_and_amateur.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/2/146_and_glasses.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/119/887_white_party.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/351_tits_getting.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/358_tits_and.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/174/847_over_store.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/453_Sexy_teen.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/656_babe_her.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/228/876_brunette_brunette.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/384_glazed_hardcore.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/496_premium_premium.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/125/947_Sexy_and.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/671_morning_lingerie.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/35/992_facial_get.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/39/247_heavy_chested.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/3/149_and_takes.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/946_her_her.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/130/768_and_lingerie.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/415_Enjoy_lovemaking.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/581_her_booty.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/198_poses_Sweet.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/138_O_by.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/740_Santoro_were.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/18/075_panties_panties.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/55/007_that_her.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/208/972_in_undressing.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/225/729_ass_flat.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/257_Orgy_multiple.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/696_cutie_fucking.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/195/963_latina_milf.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/635_and_fucked.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/202/995_kind_mechanic.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/169/960_Adorable_casting.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/36/089_taped_with.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/117/726_poses_teen.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/182/411_anal_of.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/212/977_underneath_underneath.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/237/626_cant_the.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/122/036_really_really.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/176/518_girl_poses.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/051_Tub_N.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/098_and_down.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/633_girl_fucked.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/117/756_breasts_Petite.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/381_into_into.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/169/499_coed_Amateur.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/358_Cfnm_Cfnm.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/172/040_She_.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/48/142_Lei_a.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/200_Slutty_wild.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/398_kara_wants.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/9/905_Glam_while.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/328_humongous_anika.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/237/363_their_watch.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/2/862_her_her.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/173/196_small_with.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/045_teen_slit.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/35/770_Sexy_shots.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/230/797_hot_Aneta.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/077_teen_nude.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/36/212_for_camera.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/16/129_is_heels.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/36/116_tits_teases.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/033_after_off.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/187/468_teen_poses.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/976_sexy_spreading.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/188/290_with_legs.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/9/964_Hotel_In.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/841_teenage_Britney.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/753_play_her.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/505_Teen_Teen.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/871_Jennifer_just.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/221/980_the_pinky.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/15/429_underneath_underneath.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/611_fun_some.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/237/579_public_set.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/126/806_Close_in.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/122/111_Marissa_up.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/122/156_big_teen.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/401_Pattaya_by.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/626_her_Luna.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/916_awakes_the.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/15/925_and_explains.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/14/317_Sylvanna_dykes.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/36/197_bathroom_and.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/48/898_teasingly_and.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/219/464_slit_and.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/475__in.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/343_spotted_Jimmy.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/8/137_Lacey_pussy.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/122/141_cooter_Lynn.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/951_babe_Angel.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/12/085_lesbians_lesbians.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/2/438_photos_in.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/304_Big_boobs.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/35/948_off_off.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/116/272_lips_of.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/870_son_step.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/134/366_her_brunette.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/188_teen_Cute.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/211/768_Teen_show.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/396_showing_in.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/15/589_handjob_handjob.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/066_in_tiny.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/44/744_pickups_public.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/119/857_other_tits.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/193/461_agent_public.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/117/906_pics_these.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/13/162_on_can.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/144_lovers_teasing.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/170/484_Enticing_Enticing.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/2/266_Horny_alone.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/828_with_button.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/686_Nora_all.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/438_Smiley_blonde.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/967_Italia_Italia.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/546_trueamateurmodelscom_Amy.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/565_public_32.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/235/234_All_All.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/196/997_agent_set.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/14/112_MILF_Dick.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/56/168_gfs_Amateur.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/334_set_public.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/122/126_cowgirl_sex.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/36/128_blonde_gives.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/49/268_sexy_housewife.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/180/099__shows.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/551_amateur_cunt.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/37/048_her_breasts.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/468_in_undressing.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/768_amateur_bed.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/120/299_multiple_multiple.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/349_to_landlord.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/239/808_her_on.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/16/026_undressing_in.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/130/389_set_agent.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/239/699_Samantha_Suduces.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/237/772_pays_Mellanie.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/768_in_teen.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/713_in_big.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/56/553_to_to.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/524_teenage_Bangs.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/181/984_Mayhem_Maryjane.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/128/871_time_cunts.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/35/680_spreading_spreading.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/11/574_shows_blowjob.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/17/046_girl_modelling.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/52/503_is_making.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/234/918_with_tits.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/186/372_of_pictures.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/125/992_found_and.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/118/906__porn.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/35/890_flawless_her.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/504_on_lesbian.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/117/696_girl_redhead.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/207/126_lingerie_show.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/44/326_Fuckable_her.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/237/555_Cock_Cock.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/916_with_gets.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/8/047_Amateur_deep.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/10/023_blonde_the.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/105__.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/734_amateur_posing.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/783_and_sucking.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/184/538_gets_up.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/186/291_hot_round.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/35/920_pot_getting.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/37/009_revenge_gf.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/14/084_is_mouth.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/221/975_lips_her.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/639_babe_Baby.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/669_other_amateur.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/17/737_naked_naked.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/219/868_sucks_boyfriends.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/35/905_masturbates_babe.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/229/463_after_teen.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/35/710_Naughty_getting.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/828_girl_Amazing.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/170/679_and_and.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/783_tanned_slit.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/224/621_in_ass.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/0/110_double_double.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/202/078_an_ducati.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/220/324_poses_with.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/36/019_Indian_sleazy.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/172/155_Gorgeous_young.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/36/048_loves_Aubrey.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/239/763_to_on.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/178/691_teasing_sexy.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/172/140_new_new.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/596_having_having.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/193/288_amarna_Hairy.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/957_dick_a.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/55/022_set_cel.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/376_set_xx.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/171/873_desk_hot.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/8/283_asshole_Mommy.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/1/210__239.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/121/813_demonstrates_her.jpg",
  "http://sigmapics.net/images/xxxsexpic.net/170/491_honeys_and.jpg",
]

def get_json(url, **kwargs):
    response = requests.get(url, timeout=TIMEOUT, **kwargs)
    response.raise_for_status()
    return response

def image_from_page(url):
    """Return a public image URL found on a direct image URL or HTML page."""
    try:
        r = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0"},
            stream=True,
            allow_redirects=True,
        )
        content_type = r.headers.get("Content-Type", "").lower()

        if r.ok and content_type.startswith("image/"):
            final_url = r.url
            r.close()
            return final_url

        r.close()

        page = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True,
        )
        if not page.ok:
            return None

        soup = BeautifulSoup(page.text, "html.parser")

        # Prefer social preview images.
        for key in ("og:image", "twitter:image", "twitter:image:src"):
            tag = soup.find("meta", attrs={"property": key}) or soup.find(
                "meta", attrs={"name": key}
            )
            if tag and tag.get("content"):
                candidate = urljoin(page.url, tag["content"].strip())
                if is_image(candidate):
                    return candidate

        # Otherwise inspect a few normal image tags.
        for tag in soup.find_all("img")[:30]:
            candidate = (
                tag.get("src")
                or tag.get("data-src")
                or tag.get("data-original")
            )
            if candidate:
                candidate = urljoin(page.url, candidate.strip())
                if is_image(candidate):
                    return candidate

    except requests.RequestException:
        log.info("Could not inspect URL: %s", url)
    return None

def is_image(url):
    try:
        r = requests.get(
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": "Mozilla/5.0"},
            stream=True,
            allow_redirects=True,
        )
        ctype = r.headers.get("Content-Type", "").lower()
        length = r.headers.get("Content-Length")
        okay = r.ok and ctype.startswith("image/")
        if length and int(length) > MAX_IMAGE_BYTES:
            okay = False
        r.close()
        return okay
    except (requests.RequestException, ValueError):
        return False

def read_links():
    return [
        link.strip()
        for link in IMAGE_LINKS
        if link.strip() and not link.strip().startswith("#")
    ]

def telegram(method, payload):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"
    r = requests.post(url, json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error: {data}")
    return data.get("result")

def send_text(chat_id, text, reply_to=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_to:
        payload["reply_to_message_id"] = reply_to
    telegram("sendMessage", payload)

def handle_update(update):
    message = update.get("message") or update.get("edited_message")
    if not message:
        return

    text = (message.get("text") or "").strip()
    if not text:
        return

    # Accept /image and /image@YourBotName in groups.
    command = text.split()[0].split("@")[0].lower()
    if command != "/image":
        return

    chat_id = message.get("chat", {}).get("id")
    reply_to = message.get("message_id")
    if not chat_id:
        return

    try:
        links = read_links()
        random.shuffle(links)

        for link in links:
            image_url = image_from_page(link)
            if image_url:
                # Telegram fetches the public image URL and sends one photo.
                telegram("sendPhoto", {
                    "chat_id": chat_id,
                    "photo": image_url,
                    "reply_to_message_id": reply_to,
                })
                return

        send_text(chat_id, "No working image was found in the GitHub list.", reply_to)

    except Exception:
        log.exception("Image command failed")
        send_text(chat_id, "Sorry, I couldn't fetch an image right now. Please try again.", reply_to)

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"Telegram image bot webhook is running."
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        # No webhook secret is required in this simplified setup.
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            update = json.loads(raw.decode("utf-8"))
            if isinstance(update, dict):
                handle_update(update)
        except Exception:
            log.exception("Webhook request failed")

        # Acknowledge Telegram so it does not repeatedly retry this update.
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"ok")
