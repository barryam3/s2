import { Component, Input } from '@angular/core';
import { Song } from '../song.service';
import { LinkService } from '../link.service';
import { filterInPlace } from '../../utils';

@Component({
  selector: 'app-links',
  templateUrl: './links.component.html',
  styleUrls: ['./links.component.scss'],
})
export class LinksComponent {
  @Input() song: Song;

  newLinkURL = '';
  newLinkDescription = '';

  constructor(private linkService: LinkService) { }

  deleteLink(linkID: number) {
    this.linkService.deleteLink(linkID).subscribe(() => {
      filterInPlace(this.song.links, link => link.id !== linkID);
    });
  }

  addLink() {
    this.linkService.addLink(this.song.id, this.newLinkURL, this.newLinkDescription)
      .subscribe(link => {
        this.song.links.push(link);
        this.newLinkURL = '';
        this.newLinkDescription = '';
      });
  }

}
