sources = ["https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExODdxaGYyOXNkd3E5eXp6ZHpmaHRpMTl2ZzVwbmg4NzB2YmxkdWg1MiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7btZ3T6y3JTmjg4w/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExOG5qM3AwanJldjhpMTU5b3V0cTdmazAxdGliYXZobjFxMWJkbDRqYyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3og0IV7MOCfnm85iRa/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbnY3c21heTVxOXc4Y25zdm8wd2Fjcnkwc2hmbm0xNWY0ajhhMHpkeCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/GEzD69bVIQO40/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExcXljNmNmbjd1czhpZnU3eWI0NTZjcXBkZGpsYTlzZTd6OWsyaG5obCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xTk9ZPDCfGw1RALwxq/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNm03ODhmcGpnZ2YzbmE0ZG11ejJ0b294b2JjdGczbWFzNDI4djhodSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/CuKEZdZ3V01gI/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnhqczZpeW52cHhsOGlrcHI1YWp1ZjJuZW5sajRja3M1Y2hpMDllaiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6A8PRrChk5u2k/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaTZxZ3ZocGEydDNqaDltNzU5YXV4dG5sYXc5OWdlM3FkeW05aHNsdSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3owypdCOTCXmq33MCQ/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDVudHdwMm50anFnYzR6Y3N3b3Jhc2czYzhuN3F2ZjhudGdmeWpjayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YRjZCWEIqMuEU/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2hqenBlajE2Mnhicmw0dW51OGhnd3EzazVqY2h5djJ0djNwNmRlOSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3rgXBFFa1uk6ChdJVm/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExbWJ4OG8yN3Zna3h6a3Qzb2syd2gyOHN6MGhjanBieDF3bDNka2p1biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Yv66XRlbWCuQw/giphy.gif",
           "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjR1emVkdWdkcDV5d2Q2NG5nM25sOWRyYzRtZHF1cGpkMDNscmc4OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/10qHEa7ShsJ8I0/giphy.gif"];

let gif = document.getElementById('gif');
// change gif source every minute
let i = 0;
setInterval(() => {
    gif.src = sources[i];
    i = (i + 1) % sources.length;
}, 1000 * 60 * 5);