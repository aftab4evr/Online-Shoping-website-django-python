class Bootstrap4Adapter {

    constructor(jQuery, hiddenSelect, options) {
        const defaults = {
            //usePopper: true,
            selectedPanelDefMinHeight: 'calc(2.25rem + 2px)',
            selectedPanelReadonlyBackgroundColor: '#e9ecef',
            selectedPanelBoxShadow: '0 0 0 0.2rem rgba(0, 123, 255, 0.25)',
            selectedPanelFocusBorderColor: '#80bdff',
            selectedPanelFocusValidBoxShadow: ' 0 0 0 0.2rem rgba(40, 167, 69, 0.25)',
            selectedPanelFocusInvalidBoxShadow: '0 0 0 0.2rem rgba(220, 53, 69, 0.25)',
            filterInputColor: '#495057'
        };
        this.options = jQuery.extend({}, defaults, options);
        this.jQuery=jQuery;
        this.hiddenSelect=hiddenSelect;

        this.containerClass= 'dashboardcode-bsmultiselect';
        this.dropDownMenuClass= 'dropdown-menu';
        this.dropDownItemClass= 'px-2';
        this.dropDownItemHoverClass= 'text-primary bg-light';
        this.selectedPanelClass= 'form-control';
        this.selectedPanelStyle= {'margin-bottom': '0'};
        this.selectedItemClass= 'badge'; 
        this.selectedItemStyle= {'padding-left': '0px', 'line-height': '1rem'};
        this.removeSelectedItemButtonClass= 'close';
        this.removeSelectedItemButtonStyle= {'line-height': '1rem', 'font-size':'1.3rem'};
    }

    CreateSelectedItemContent($selectedItem, itemText, removeSelectedItem){
        $selectedItem.addClass(this.selectedItemClass);
        $selectedItem.css(this.selectedItemStyle);
            
        let $text = this.jQuery(`<span>${itemText}</span>`)
        let $buttom = this.jQuery('<button aria-label="Close" tabIndex="-1" type="button"><span aria-hidden="true">&times;</span></button>');

        $buttom.addClass(this.removeSelectedItemButtonClass);
        $buttom.css(this.removeSelectedItemButtonStyle);

        $buttom.on("click", removeSelectedItem);
        $text.appendTo($selectedItem);
        $buttom.appendTo($selectedItem); 
    }

    CreateDropDownItemContent($dropDownItem, optionId, itemText, isSelected){
        let checkBoxId = `${this.containerClass}-${this.hiddenSelect.name.toLowerCase()}-generated-id-${optionId.toLowerCase()}`;
        let checked = isSelected ? "checked" : "";

        let $dropDownItemContent= this.jQuery(`<div class="custom-control custom-checkbox">
                <input type="checkbox" class="custom-control-input" id="${checkBoxId}" ${checked}>
                <label class="custom-control-label" for="${checkBoxId}">${itemText}</label>
        </div>`)
        $dropDownItemContent.appendTo($dropDownItem);
        $dropDownItem.addClass(this.dropDownItemClass)
        let $checkBox = $dropDownItem.find(`INPUT[type="checkbox"]`);
        let adoptDropDownItem = (isSelected) => {
            $checkBox.prop('checked', isSelected);
        }
        return adoptDropDownItem;
    }

    Init($container, $selectedPanel, $filterInputItem, $filterInput, $dropDownMenu){

        $container.addClass(this.containerClass);


            $selectedPanel.addClass(this.selectedPanelClass);
            $selectedPanel.css(this.selectedPanelStyle);
            $selectedPanel.css({ "min-height" : this.options.selectedPanelMinHeight });

        let $hiddenSelect = this.jQuery(this.hiddenSelect);
        if ($hiddenSelect.hasClass("is-valid")){
            $selectedPanel.addClass("is-valid");
        }
        
        if ($hiddenSelect.hasClass("is-invalid")){
            $selectedPanel.addClass("is-invalid");
        }

        $dropDownMenu.addClass(this.dropDownMenuClass);
        $filterInput.css("color", this.options.filterInputColor);
    }

    Enable($selectedPanel, isEnabled){
        if(isEnabled){
            let inputId = this.hiddenSelect.id;
            let $formGroup = this.jQuery(this.hiddenSelect).closest('.form-group');
            
            if ($formGroup.length == 1) {
                let $label = $formGroup.find(`label[for="${inputId}"]`);
                let f = $label.attr('for');
                let $filterInput = $selectedPanel.find('input');
                if (f == this.hiddenSelect.id) {
                    let id = `${this.containerClass}-generated-filter-id-${this.hiddenSelect.id}`;
                    $filterInput.attr('id', id);
                    $label.attr('for', id);
                }
            }
        }
        else{
            $selectedPanel.css({"background-color": this.dropDownItemHoverClass});
            $selectedPanel.find('BUTTON').prop("disabled", true).off();
        }
    }

    Hover($dropDownItem, isHover){
        if (isHover)
            $dropDownItem.addClass(this.options.dropDownItemHoverClass);
        else
            $dropDownItem.removeClass(this.options.dropDownItemHoverClass);
    }

    FilterClick(event){
        return !(event.target.nodeName == "BUTTON" || (event.target.nodeName == "SPAN" && event.target.parentElement.nodeName == "BUTTON"))
    }

    Focus($selectedPanel, isFocused){
        if (isFocused){
                if ($selectedPanel.hasClass("is-valid")){
                    $selectedPanel.css("box-shadow", this.options.selectedPanelValidBoxShadow);              
                } else if ($selectedPanel.hasClass("is-invalid")){
                    $selectedPanel.css("box-shadow", this.options.selectedPanelInvalidBoxShadow);
                } else {
                    $selectedPanel
                        .css("box-shadow", this.options.selectedPanelBoxShadow)
                        .css("border-color", this.options.selectedPanelBorderColor);
                }
        }else{
            $selectedPanel.css("box-shadow", "" ).css("border-color", "")
        }
    }
}

export default Bootstrap4Adapter;