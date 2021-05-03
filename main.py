from bin.scraper import Omni


if __name__ == '__main__':
    scraper = Omni(
        base_url='https://www.dallascounty.org/jaillookup/searchByName',
        specs={
            'pagination': True,
            'pages_element': '',
            'error_message': 'No records were found using the search criteria provided',
            'fields': {
                'firstName': 'input',
                'lastName': 'input',
                'race': 'select',
                'sex': 'select'
            },
            'buttonText': 'Search By Prisoner Info'
        }
    )
    