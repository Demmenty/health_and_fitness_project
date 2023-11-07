// блоки шестеронок с текстом - секция what
const whatSectionBlocks = document.querySelectorAll(".what_section_block");

// первоначальная настройка текстов у шестеренок
window.onload = function() {
    whatSectionBlocks.forEach(block => {
        let whatTxt = block.querySelector(".txt_what");
        let visibleTxt = block.querySelector("p");
        visibleTxt.style.height = whatTxt.offsetHeight + 3 + "px";
    });
}

// коррекция текстов при изменении размера окна
window.addEventListener('resize', function() {
    whatSectionBlocks.forEach(block => {
        let whatTxt = block.querySelector(".txt_what");
        let howTxt = block.querySelector(".txt_how");
        let visibleTxt = block.querySelector("p");

        if (block.classList.contains('open')) {
            whatTxt.style.marginTop = "-" + (whatTxt.offsetHeight + 24) + "px";
            visibleTxt.style.height = howTxt.offsetHeight + 3 + "px";
        }
        else {
            visibleTxt.style.height = whatTxt.offsetHeight + 3 + "px";
        }
    });
}, true);

// смена текстов шестеренок при наведении мыши на текст блока
$(".what_section_block p")
    .on("mouseenter", function(){
        block = $(this).closest(".what_section_block");
        whatTxt = block.find(".txt_what");
        howTxt = block.find(".txt_how");
        visibleTxt = $(this);
        dumbbell = block.find(".dumbbell_bottom");
        gear = block.find('.gear_lg');

        visibleTxt.css('height', (howTxt.outerHeight() + 3 + "px"));
        whatTxt.css('marginTop', ("-" + (whatTxt.outerHeight() + 24) + "px"));
        gear.addClass('turned');
        dumbbell.addClass('down');
    })
    .on("mouseleave", function(){
        block = $(this).closest(".what_section_block");
        whatTxt = block.find(".txt_what");
        visibleTxt = $(this);
        dumbbell = block.find(".dumbbell_bottom");
        gear = block.find('.gear_lg');

        if (!(block.hasClass('open'))) {
            visibleTxt.css('height', whatTxt.outerHeight() + 3 + "px"); 
            whatTxt.css('marginTop', "");
            gear.removeClass('turned');
            dumbbell.removeClass('down');
        }
    });
    
// смена текстов шестеренок при наведении мыши на шестеренку блока
$(".what_section_block .gear_lg")
    .on("mouseenter", function() {
        block = $(this).closest(".what_section_block");
        whatTxt = block.find(".txt_what");
        howTxt = block.find(".txt_how");
        visibleTxt = block.find("p");
        dumbbell = block.find(".dumbbell_bottom");
        gear = block.find('.gear_lg');

        visibleTxt.css('height', (howTxt.outerHeight() + 3 + "px"));
        whatTxt.css('marginTop', ("-" + (whatTxt.outerHeight() + 24) + "px"));
        gear.addClass('turned');
        dumbbell.addClass('down');
    })
    .on("mouseleave", function() {
        block = $(this).closest(".what_section_block");
        whatTxt = block.find(".txt_what");
        howTxt = block.find(".txt_how");
        visibleTxt = block.find("p");
        dumbbell = block.find(".dumbbell_bottom");
        gear = block.find('.gear_lg');

        if (!(block.hasClass('open'))) {
            visibleTxt.css('height', whatTxt.outerHeight() + 3 + "px"); 
            whatTxt.css('marginTop', "");
            gear.removeClass('turned');
            dumbbell.removeClass('down');
        }
    });


// изменение текста шестеренок c фиксацией при клике
function openWhatSectionBlock(event) {
    const block = event.target.closest('.what_section_block');
    const whatTxt = block.querySelector(".txt_what");
    const howTxt = block.querySelector(".txt_how");
    const visibleTxt = block.querySelector("p");
    const gear = block.querySelector(".gear_lg");
    const dumbbell = block.querySelector(".dumbbell_bottom");

    if (block.classList.contains('open')) {
        whatTxt.style.marginTop = "";
        visibleTxt.style.height = whatTxt.offsetHeight + "px";
        gear.classList.remove('turned');
        dumbbell.classList.remove('down');
        block.classList.remove('open');
    }
    else {
        block.classList.add('open');
        gear.classList.add('turned');
        dumbbell.classList.add('down');
        whatTxt.style.marginTop = "-" + (whatTxt.offsetHeight + 24) + "px";
        visibleTxt.style.height = howTxt.offsetHeight + "px";
    }
}
